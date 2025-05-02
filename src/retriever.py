"""Module for retrieving relevant document chunks."""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)
from src.vectorstore.vector_store import VectorStore

class Retriever:
    """Handles retrieval of relevant document chunks."""
    
    def __init__(self, vectorstore_path: str = "vectorstore"):
        """Initialize with vector store instance."""
        self.vectorstore = VectorStore(vectorstore_path)

    def store_documents(self, chunks: List[Dict]) -> bool:
        """
        Store document chunks in vector store.
        
        Args:
            chunks: List of document chunks with content and metadata
            
        Returns:
            True if storage succeeded
        """
        logger.info(f"Storing {len(chunks)} document chunks")
        return self.vectorstore.store_documents(chunks)
        
    def retrieve_relevant_chunks(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieve k most relevant document chunks for query.
        
        Args:
            query: The search query
            k: Number of results to return
            
        Returns:
            List of relevant chunks with content and metadata
        """
        logger.info(f"Retrieving {k} chunks for query: {query}")
        results = self.vectorstore.query(query, n_results=k)
        logger.info(f"Retrieved {len(results)} chunks before filtering")
        return self.filter_results(results)
        
    def filter_results(self, results: List[Dict]) -> List[Dict]:
        """
        Filter retrieved results for relevance.
        Currently filters out results with distance > 1.0.
        
        Args:
            results: List of retrieved chunks
            
        Returns:
            Filtered list of chunks
        """
        filtered = [r for r in results if r['distance'] <= 1.0]
        logger.info(f"Filtered from {len(results)} to {len(filtered)} chunks")
        return filtered
