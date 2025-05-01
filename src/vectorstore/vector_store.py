"""Module for handling document embeddings and vector storage."""
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class VectorStore:
    """Handles document embeddings and vector storage."""
    
    def __init__(self, persist_dir: str = "vectorstore"):
        """Initialize vector store with persistent storage."""
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_dir,
                chroma_db_impl="duckdb+parquet"
            )
        )
        self.collection = self.client.get_or_create_collection("documents")
        
    def generate_embeddings(self, chunks: List[Dict]) -> List[List[float]]:
        """Generate embeddings for document chunks."""
        contents = [chunk['content'] for chunk in chunks]
        return self.embedding_model.encode(contents).tolist()
        
    def store_documents(self, chunks: List[Dict]) -> None:
        """Store document chunks with embeddings in vector database."""
        embeddings = self.generate_embeddings(chunks)
        ids = [f"{chunk['metadata']['source']}-{chunk['metadata']['chunk_start']}" 
               for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        contents = [chunk['content'] for chunk in chunks]
        
        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        
    def persist(self) -> None:
        """Persist the vector store to disk."""
        self.client.persist()
