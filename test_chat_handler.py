"""Test script for ChatHandler functionality."""
from src.chat_handler import ChatHandler
from unittest.mock import MagicMock

def test_chat_handler():
    """Test end-to-end chat processing."""
    # Mock configuration
    config = {
        'model_path': 'test_model',
        'docs_dir': 'test_docs',
        'vectorstore_path': 'test_vectorstore'
    }
    
    # Create handler with mocked components
    handler = ChatHandler(config)
    
    # Mock model manager
    handler.model = MagicMock()
    handler.model.generate.return_value = "Python is a versatile programming language."
    
    # Mock retriever
    handler.retriever = MagicMock()
    handler.retriever.retrieve_relevant_chunks.return_value = [
        {
            'content': 'Python is used for web development and data science.',
            'metadata': {'source': 'python.md', 'chunk_start': 0},
            'distance': 0.3
        }
    ]
    
    # Test query processing
    result = handler.process_query("What is Python?")
    print("ChatHandler results:")
    print(f"Response: {result['response']}")
    print(f"Sources: {result['sources']}")
    print(f"Tokens used: {result['tokens']}")
    
    # Test response formatting
    test_response = "Test response"
    test_sources = [{'source': 'doc1.md'}, {'source': 'doc2.md'}]
    formatted = handler.format_response(test_response, test_sources)
    print(f"\nFormatted response:\n{formatted}")

if __name__ == "__main__":
    test_chat_handler()
