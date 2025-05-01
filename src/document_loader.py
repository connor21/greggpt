"""Module for loading and processing markdown documents."""
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading and preprocessing of markdown documents."""
    
    def __init__(self, docs_dir: str):
        """Initialize with directory containing markdown files."""
        logger.info(f"Initializing DocumentLoader with directory: {docs_dir}")
        self.docs_dir = Path(docs_dir)
        logger.info(f"Document directory set to: {self.docs_dir}")
        
    def load_documents(self) -> List[Dict]:
        """Load and parse all markdown files in directory.
        
        Returns:
            List[Dict]: List of documents with keys: 'content', 'metadata'
        """
        logger.info(f"Loading markdown documents from {self.docs_dir}")
        documents = []
        md_files = list(self.docs_dir.glob('*.md'))
        logger.info(f"Found {len(md_files)} markdown files")
        
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append({
                    'content': content,
                    'metadata': {
                        'source': str(md_file),
                        'file_name': md_file.name
                    }
                })
        return documents
        
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Split documents into smaller chunks for processing.
        
        Args:
            documents: List of documents from load_documents()
            
        Returns:
            List[Dict]: List of chunks with same structure as input
        """
        logger.info(f"Chunking {len(documents)} documents")
        chunks = []
        chunk_size = 1000  # characters
        overlap = 200
        total_chars = sum(len(d['content']) for d in documents)
        logger.info(f"Total characters to process: {total_chars}")
        
        for doc in documents:
            content = doc['content']
            metadata = doc['metadata']
            
            start = 0
            while start < len(content):
                end = min(start + chunk_size, len(content))
                chunk = content[start:end]
                
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        **metadata,
                        'chunk_start': start,
                        'chunk_end': end
                    }
                })
                start = end - overlap
                
        return chunks
