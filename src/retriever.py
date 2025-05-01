"""Module for retrieving relevant document chunks."""
from typing import List, Dict
from src.vectorstore.vector_store import VectorStore

class Retriever:
    """Handles retrieval of relevant document chunks."""
    
    def __init__(self, vectorstore_path: str = "vectorstore"):
        """Initialize with vector store instance."""
        self.vectorstore = VectorStore(vectorstore_path)
        
    def retrieve_relevant_chunks(self, query: str, k: int = 3) -> List[Dict]:
        """
        Retrieve k most relevant document chunks for query.
        
        Args:
            query: The search query
            k: Number of results to return
            
        Returns:
            List of relevant chunks with content and metadata
        """
        results = self.vectorstore.query(query, n_results=k)
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
        return [r for r in results if r['distance'] <= 1.0]
