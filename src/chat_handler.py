"""Module for handling chat interactions."""
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)
from src.models.model_manager import ModelManager
from src.document_loader import DocumentLoader
from src.retriever import Retriever

class ChatHandler:
    """Coordinates chat interactions between components."""
    
    def __init__(self, config: Dict):
        """Initialize with configuration dictionary."""
        logger.info("Initializing ChatHandler with config")
        self.config = config
        self.model = ModelManager(config)
        self.loader = DocumentLoader(
            config['docs_dir'],
            chunk_size=config['chunk_size'],
            chunk_overlap=config['chunk_overlap']
        )
        self.retriever = Retriever(config['vectorstore_path'])
        
        # Load and store documents at startup
        logger.info("Loading and storing documents")
        documents = self.loader.load_documents()
        chunks = self.loader.chunk_documents(documents)
        self.retriever.store_documents(chunks)
        logger.info(f"Loaded {len(documents)} documents and stored {len(chunks)} chunks")
        
        logger.info("ChatHandler components initialized")
        
    def process_query(self, query: str) -> Dict:
        """
        Process user query through full RAG pipeline.
        
        Args:
            query: User's input question/message
            
        Returns:
            Dictionary containing:
            - response: Generated answer
            - sources: List of source documents used
            - tokens: Token usage information
        """
        logger.info(f"Processing query: {query}")
        
        # Handle empty query
        if not query.strip():
            return {
                'response': "Please provide a valid query.",
                'sources': [],
                'tokens': 0
            }
            
        # Retrieve relevant context
        context_chunks = self.retriever.retrieve_relevant_chunks(query)
        logger.info(f"Retrieved {len(context_chunks)} context chunks")
        
        # Format prompt with context
        prompt = self._format_prompt(query, context_chunks)
        
        # Ensure model is loaded and get response
        if not hasattr(self.model, 'llm') or self.model.llm is None:
            logger.info("Loading LLM model")
            self.model.load_model()
        logger.info("Generating response from LLM")
        response = self.model.generate_response(prompt)
        logger.info(f"Generated response with {len(response.split())} tokens")
        
        return {
            'response': self.format_response(response, context_chunks),
            'sources': [chunk['metadata'] for chunk in context_chunks],
            'tokens': len(prompt.split()) + len(response.split())
        }
        
    def _format_prompt(self, query: str, context: List[Dict]) -> str:
        """Format prompt with context and query."""
        context_str = "\n".join(
            f"Source: {c['metadata']['source']}\nContent: {c['content']}"
            for c in context
        )
        return f"""Answer the question using only the provided context.
        
Context:
{context_str}

Question: {query}
Answer:"""
        
    def format_response(self, response: str, sources: List[Dict]) -> str:
        """
        Format response with enhanced source citations.
        
        Args:
            response: Raw LLM response
            sources: List of source metadata dictionaries
            
        Returns:
            Formatted response with clean citations and references
        """
        if not sources:
            return response

        # Format sources using utility function
        formatted_sources = self._format_sources(sources)
        
        # Add citations in the text
        cited_response = response
        for i, source in enumerate(sources, 1):
            cited_response = cited_response.replace(
                source.get('content', ''),
                f"{source.get('content', '')} [^{i}]"
            )

        return f"{cited_response}\n\n### Sources\n{formatted_sources}"

    def _format_sources(self, sources: List[Dict]) -> str:
        """
        Format source references into clean bullet points.
        
        Args:
            sources: List of source metadata dictionaries
            
        Returns:
            Formatted markdown string with clean source references
        """
        formatted = []
        for i, source in enumerate(sources, 1):
            # Clean source name (remove path and extension)
            source_name = source.get('source', '')
            if not source_name and 'metadata' in source:
                source_name = source['metadata'].get('source', '')
            
            if not source_name:
                logger.warning(f"Missing source name in document metadata: {source}")
                source_name = "Document"
            else:
                if '/' in source_name:
                    source_name = source_name.split('/')[-1]
                if '.' in source_name:
                    source_name = source_name.split('.')[0]
                source_name = source_name.replace('_', ' ').title()

            # Get excerpt
            excerpt = source.get('content', '')[:100] + ('...' if len(source.get('content', '')) > 100 else '')
            
            formatted.append(
                f"- [^{i}] **{source_name}**\n  {excerpt}"
            )
            
        return "\n".join(formatted)
