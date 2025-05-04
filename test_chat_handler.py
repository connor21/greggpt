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

def test_format_sources(mock_config):
    """Test source formatting utility."""
    with patch('src.chat_handler.DocumentLoader'):
        handler = ChatHandler(mock_config)
    
    # Test with normal sources
    sources = [
        {
            'source': 'path/to/doc1.md',
            'content': 'First source content',
            'metadata': {'page': 42}
        },
        {
            'source': 'another/doc2.pdf',
            'content': 'Second source content',
            'metadata': {'chunk_start': 10, 'chunk_end': 20}
        }
    ]
    
    formatted = handler._format_sources(sources)
    assert "Doc1" in formatted
    assert "Doc2" in formatted
    assert "- [^1]" in formatted
    assert "- [^2]" in formatted
    assert "First source content" in formatted
    assert "Second source content" in formatted
    assert "path/to" not in formatted
    assert "another/" not in formatted

    # Test with missing source name
    no_source = [{'content': 'Test content', 'metadata': {}}]
    formatted = handler._format_sources(no_source)
    assert "Document" in formatted
    assert "Test content" in formatted

    # Test with source in metadata only
    meta_source = [{'metadata': {'source': 'meta_doc.txt'}}]
    formatted = handler._format_sources(meta_source)
    assert "Meta Doc" in formatted

def test_format_response(mock_config):
    """Test enhanced response formatting with citations."""
    with patch('src.chat_handler.DocumentLoader'):
        handler = ChatHandler(mock_config)
    
    response = "Test response with content"
    sources = [
        {
            'source': 'doc1.md',
            'content': 'content',
            'metadata': {}
        }
    ]
    
    formatted = handler.format_response(response, sources)
    
    # Verify response contains original text
    assert response in formatted
    
    # Verify new citation format
    assert "[^1]" in formatted
    assert "### Sources" in formatted
    
    # Verify markdown bullet format
    assert "- [^1]" in formatted
    
    # Verify no technical metadata
    assert "chunk_start" not in formatted
    assert "chunk_end" not in formatted

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
