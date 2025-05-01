"""Test script for VectorStore functionality."""
from src.vectorstore.vector_store import VectorStore

def test_vector_store():
    """Test basic vector store operations."""
    vs = VectorStore("test_vectorstore")
    
    # Test data
    chunks = [
        {
            'content': 'Python is a popular programming language',
            'metadata': {'source': 'python.md', 'chunk_start': 0}
        },
        {
            'content': 'ChromaDB is a vector database for embeddings',
            'metadata': {'source': 'chroma.md', 'chunk_start': 0}
        }
    ]
    
    # Store documents
    vs.store_documents(chunks)
    
    # Query test
    results = vs.query("What is Python?")
    print("Query results:")
    for r in results:
        print(f"- {r['content']} (distance: {r['distance']:.4f})")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_vectorstore")

if __name__ == "__main__":
    test_vector_store()
