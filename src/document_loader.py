"""Module for loading and processing markdown documents."""
from pathlib import Path
from typing import List, Dict

class DocumentLoader:
    """Handles loading and preprocessing of markdown documents."""
    
    def __init__(self, docs_dir: str):
        """Initialize with directory containing markdown files."""
        self.docs_dir = Path(docs_dir)
        
    def load_documents(self) -> List[Dict]:
        """Load and parse all markdown files in directory.
        
        Returns:
            List[Dict]: List of documents with keys: 'content', 'metadata'
        """
        documents = []
        for md_file in self.docs_dir.glob('*.md'):
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
        chunks = []
        chunk_size = 1000  # characters
        overlap = 200
        
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
