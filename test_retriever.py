"""Unit tests for Retriever functionality."""
import pytest
from unittest.mock import MagicMock, patch
from src.retriever import Retriever

@pytest.fixture
def mock_vectorstore():
    """Fixture providing a mock vectorstore."""
    mock = MagicMock()
    mock.store_documents.return_value = True
    return mock

@pytest.fixture
def test_chunks():
    """Fixture providing test document chunks."""
    return [
        {
            'content': 'Python is a popular programming language',
            'metadata': {'source': 'python.md', 'chunk_start': 0}
        },
        {
            'content': 'ChromaDB is a vector database for embeddings',
            'metadata': {'source': 'chroma.md', 'chunk_start': 0}
        }
    ]

def test_retriever_initialization(mock_vectorstore):
    """Test Retriever initialization."""
    with patch('src.retriever.VectorStore', return_value=mock_vectorstore):
        retriever = Retriever("test_path")
        assert retriever.vectorstore == mock_vectorstore

def test_store_documents(mock_vectorstore, test_chunks):
    """Test document storage."""
    with patch('src.retriever.VectorStore', return_value=mock_vectorstore):
        retriever = Retriever("test_path")
        retriever.store_documents(test_chunks)
        mock_vectorstore.store_documents.assert_called_once_with(test_chunks)

def test_retrieve_relevant_chunks(mock_vectorstore):
    """Test chunk retrieval."""
    test_query = "What is Python?"
    expected_results = [
        {'content': 'Python is...', 'distance': 0.2, 'metadata': {}}
    ]
    mock_vectorstore.query.return_value = expected_results
    
    with patch('src.retriever.VectorStore', return_value=mock_vectorstore):
        retriever = Retriever("test_path")
        results = retriever.retrieve_relevant_chunks(test_query)
        assert results == expected_results
        mock_vectorstore.query.assert_called_once_with(test_query, n_results=3)

def test_filter_results():
    """Test result filtering."""
    retriever = Retriever("test_path")
    test_results = [
        {'content': 'Good match', 'distance': 0.4, 'metadata': {}},
        {'content': 'Bad match', 'distance': 1.2, 'metadata': {}}
    ]
    filtered = retriever.filter_results(test_results)
    assert len(filtered) == 1
    assert filtered[0]['content'] == 'Good match'

def test_empty_query(mock_vectorstore):
    """Test handling of empty query."""
    with patch('src.retriever.VectorStore', return_value=mock_vectorstore):
        retriever = Retriever("test_path")
        results = retriever.retrieve_relevant_chunks("")
        assert results == []
