"""Module for handling chat interactions."""
from typing import Dict, List
from src.models.model_manager import ModelManager
from src.document_loader import DocumentLoader
from src.retriever import Retriever

class ChatHandler:
    """Coordinates chat interactions between components."""
    
    def __init__(self, config: Dict):
        """Initialize with configuration dictionary."""
        self.config = config
        self.model = ModelManager(config['model_path'])
        self.loader = DocumentLoader(config['docs_dir'])
        self.retriever = Retriever(config['vectorstore_path'])
        
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
        # Retrieve relevant context
        context_chunks = self.retriever.retrieve_relevant_chunks(query)
        
        # Format prompt with context
        prompt = self._format_prompt(query, context_chunks)
        
        # Get LLM response
        response = self.model.generate(prompt)
        
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
        Format response with source citations.
        
        Args:
            response: Raw LLM response
            sources: List of source metadata dictionaries
            
        Returns:
            Formatted response with citations
        """
        if not sources:
            return response
            
        source_refs = "\n\nSources:\n" + "\n".join(
            f"- {s.get('source', str(s))}" for s in sources
        )
        return response + source_refs
