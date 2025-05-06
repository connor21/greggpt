"""Module for handling document embeddings and vector storage."""
import logging
import time
from functools import wraps
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

def timeout(seconds=30):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            if duration > seconds:
                raise TimeoutError(f"Operation timed out after {seconds} seconds")
            return result
        return wrapper
    return decorator

class VectorStore:
    """Handles document embeddings and vector storage."""
    
    def __init__(self, persist_dir: str = "vectorstore", initial_docs: List[Dict] = None):
        """Initialize vector store with persistent storage.
        
        Args:
            persist_dir: Directory to store vector data
            initial_docs: Optional documents to process on startup
        """
        self.persist_dir = persist_dir
        self._initialize_models()
        if initial_docs and not self._has_documents():
            self.store_documents(initial_docs)

    def _has_documents(self) -> bool:
        """Check if collection contains any documents."""
        return len(self.collection.get()['ids']) > 0
        
    def _initialize_models(self):
        """Initialize models with proper cleanup handling."""
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            logger.info(f"Using device: {self.embedding_model.device}")
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection("documents")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self._cleanup()
            raise
            
    def _cleanup(self):
        """Clean up resources."""
        if hasattr(self, 'embedding_model'):
            del self.embedding_model
        if hasattr(self, 'client'):
            del self.client
        if hasattr(self, 'collection'):
            del self.collection
            
    def __del__(self):
        """Destructor for cleanup."""
        self._cleanup()
        
    @timeout(seconds=60)
    def generate_embeddings(self, chunks: List[Dict]) -> List[List[float]]:
        """Generate embeddings with tqdm progress bar and timeout."""
        logger.info(f"Starting embedding generation for {len(chunks)} chunks")
        
        try:
            # Process chunks with tqdm progress bar
            embeddings = []
            for chunk in tqdm(chunks, desc="Generating embeddings", unit="chunk"):
                try:
                    embedding = self.embedding_model.encode(
                        chunk['content'],
                        show_progress_bar=False
                    ).tolist()
                    embeddings.append(embedding)
                except Exception as e:
                    logger.error(f"Failed to process chunk: {e}")
                    raise
                    
            logger.info("Successfully generated all embeddings")
            return embeddings
            
        except TimeoutError as te:
            logger.error(f"Embedding generation timed out: {te}")
            raise
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise
        
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
        
    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: The query text to search for
            n_results: Number of results to return
            
        Returns:
            List of dictionaries containing matched documents and metadata
        """
        query_embedding = self.embedding_model.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return [
            {
                'content': doc,
                'metadata': meta,
                'distance': dist
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
        ]
