"""Test script for Retriever functionality."""
from src.retriever import Retriever

def test_retriever():
    """Test basic retriever operations."""
    retriever = Retriever("test_vectorstore")
    
    # Test data - same as vector store test for consistency
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
    
    # Store documents (would normally be done by document loader)
    retriever.vectorstore.store_documents(chunks)
    
    # Test retrieval
    results = retriever.retrieve_relevant_chunks("What is Python?")
    print("Retriever results:")
    for r in results:
        print(f"- {r['content']} (distance: {r['distance']:.4f})")
    
    # Test filtering
    print("\nTesting filtering:")
    test_results = [
        {'content': 'Good match', 'distance': 0.5, 'metadata': {}},
        {'content': 'Bad match', 'distance': 1.5, 'metadata': {}}
    ]
    filtered = retriever.filter_results(test_results)
    print(f"Filtered {len(test_results)} results to {len(filtered)} good matches")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_vectorstore")

if __name__ == "__main__":
    test_retriever()
