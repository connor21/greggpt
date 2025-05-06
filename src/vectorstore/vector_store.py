"""Module for handling document embeddings and vector storage."""

import logging
import time
import uuid
from functools import wraps
from typing import List, Dict

from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


def timeout(seconds=30):
    """Timeout decorator to limit execution duration of a function."""
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
    """Handles document embeddings and vector storage using ChromaDB."""

    def __init__(self, persist_dir: str = "vectorstore"):
        """Initialize embedding model and Chroma persistent client."""
        self.persist_dir = persist_dir
        self._initialize_models()

    def _initialize_models(self):
        try:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            logger.info(f"Using embedding model on device: {self.embedding_model.device}")
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection("documents")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self._cleanup()
            raise

    def _cleanup(self):
        if hasattr(self, "embedding_model"):
            del self.embedding_model
        if hasattr(self, "client"):
            del self.client
        if hasattr(self, "collection"):
            del self.collection

    def __del__(self):
        self._cleanup()

    @timeout(seconds=60)
    def generate_embeddings(self, chunks: List[Dict]) -> List[List[float]]:
        """
        Generate embeddings for a list of document chunks.

        Args:
            chunks: List of chunks with 'content' fields.

        Returns:
            A list of embedding vectors.
        """
        logger.info(f"Generating embeddings for {len(chunks)} chunks.")
        embeddings = []

        for i, chunk in enumerate(tqdm(chunks, desc="Generating embeddings", unit="chunk")):
            try:
                content = chunk.get("content")
                if not content:
                    logger.warning(f"Chunk {i} has no content. Skipping.")
                    embeddings.append([])
                    continue

                embedding = self.embedding_model.encode(content, show_progress_bar=False).tolist()
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Embedding failed for chunk {i}: {e}")
                embeddings.append([])  # maintain position for alignment

        return embeddings

    def store_documents(self, chunks: List[Dict]) -> None:
        """
        Store document chunks with generated embeddings in the vector database.

        Args:
            chunks: List of chunk dictionaries with 'content' and 'metadata'.
        """
        if not chunks:
            logger.warning("No chunks provided for storage.")
            return

        try:
            embeddings = self.generate_embeddings(chunks)
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return

        contents, metadatas, ids, final_embeddings = [], [], [], []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            try:
                content = chunk.get("content")
                metadata = chunk.get("metadata", {})

                if not content or not embedding:
                    logger.warning(f"Skipping chunk {i}: missing content or empty embedding.")
                    continue

                # ID aus Metadaten oder UUID fallback
                source = metadata.get("source")
                chunk_start = metadata.get("chunk_start")
                chunk_id = f"{source}-{chunk_start}" if source and chunk_start is not None else str(uuid.uuid4())

                contents.append(content)
                metadatas.append(metadata)
                ids.append(chunk_id)
                final_embeddings.append(embedding)

            except Exception as e:
                logger.error(f"Error processing chunk {i}: {e}")
                continue

        if not ids:
            logger.error("No valid document chunks to store. Aborting storage.")
            return

        try:
            logger.info(f"Storing {len(ids)} documents in vectorstore.")
            self.collection.add(
                documents=contents,
                metadatas=metadatas,
                embeddings=final_embeddings,
                ids=ids
            )
            logger.info("Documents successfully stored in vectorstore.")
        except Exception as e:
            logger.error(f"Failed to add documents to vectorstore: {e}")

    def query(self, query_text: str, n_results: int = 3) -> List[Dict]:
        """
        Query the vector store for similar documents.

        Args:
            query_text: The search string.
            n_results: Number of top matches to return.

        Returns:
            List of dictionaries with content, metadata, and similarity distance.
        """
        try:
            query_embedding = self.embedding_model.encode(query_text).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return []
