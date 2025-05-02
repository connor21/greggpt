"""Unit tests for ChatHandler functionality."""
import pytest
from unittest.mock import MagicMock, patch
from src.chat_handler import ChatHandler

@pytest.fixture
def mock_config():
    """Fixture providing test configuration."""
    return {
        'model_path': 'test_model',
        'docs_dir': 'test_docs',
        'vectorstore_path': 'test_vectorstore',
        'chunk_size': 1000,
        'chunk_overlap': 200
    }

@pytest.fixture
def mock_components():
    """Fixture providing mocked model and retriever."""
    model = MagicMock()
    model.generate_response.return_value = "Mocked response"
    
    retriever = MagicMock()
    retriever.retrieve_relevant_chunks.return_value = [
        {
            'content': 'Mocked content',
            'metadata': {'source': 'test.md'},
            'distance': 0.2
        }
    ]
    
    return model, retriever

def test_chat_handler_initialization(mock_config):
    """Test ChatHandler initialization."""
    with patch('src.chat_handler.ModelManager'), \
         patch('src.chat_handler.Retriever'), \
         patch('src.chat_handler.DocumentLoader') as mock_loader:
        handler = ChatHandler(mock_config)
        assert handler.config == mock_config
        assert hasattr(handler, 'model')
        assert hasattr(handler, 'retriever')
        mock_loader.assert_called_once_with(
            mock_config['docs_dir'],
            chunk_size=mock_config['chunk_size'],
            chunk_overlap=mock_config['chunk_overlap']
        )

def test_process_query(mock_config, mock_components):
    """Test query processing."""
    model, retriever = mock_components
    with patch('src.chat_handler.ModelManager', return_value=model), \
         patch('src.chat_handler.Retriever', return_value=retriever):
        handler = ChatHandler(mock_config)
        result = handler.process_query("test query")
        
        assert isinstance(result, dict)
        assert 'response' in result
        assert 'sources' in result
        assert 'tokens' in result
        retriever.retrieve_relevant_chunks.assert_called_once_with("test query")
        model.generate_response.assert_called_once()

def test_format_response():
    """Test response formatting."""
    handler = ChatHandler({
        'model_path': 'test',
        'docs_dir': 'test',
        'vectorstore_path': 'test',
        'chunk_size': 1000,
        'chunk_overlap': 200
    })
    response = "Test response"
    sources = [{'source': 'doc1.md'}, {'source': 'doc2.md'}]
    formatted = handler.format_response(response, sources)
    
    assert response in formatted
    assert all(src['source'] in formatted for src in sources)
    assert "Sources:" in formatted

def test_empty_query(mock_config, mock_components):
    """Test handling of empty query."""
    model, retriever = mock_components
    with patch('src.chat_handler.ModelManager', return_value=model), \
         patch('src.chat_handler.Retriever', return_value=retriever):
        handler = ChatHandler(mock_config)
        result = handler.process_query("")
        
        assert isinstance(result, dict)
        assert 'response' in result
        retriever.retrieve_relevant_chunks.assert_not_called()
        model.generate_response.assert_not_called()
