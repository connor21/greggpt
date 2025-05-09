"""Module for loading and processing markdown documents."""
import logging
import time
from pathlib import Path
from typing import List, Dict, Optional, Callable

logger = logging.getLogger(__name__)

WATCHDOG_AVAILABLE = False
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    logger.warning("watchdog package not available - file watching disabled")

if WATCHDOG_AVAILABLE:
    class MarkdownFileHandler(FileSystemEventHandler):
        """Handler for markdown file system events."""
        
        def __init__(self, callback: Callable[[Path], None]):
            self.callback = callback
            
        def on_created(self, event):
            if not event.is_directory and event.src_path.endswith('.md'):
                self.callback(Path(event.src_path))
                
        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith('.md'):
                self.callback(Path(event.src_path))

class DocumentLoader:
    """Handles loading and preprocessing of markdown documents."""
    
    def __init__(self, docs_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.observer: Optional[Observer] = None
        """Initialize with directory and chunking parameters.
        
        Args:
            docs_dir: Directory containing markdown files
            chunk_size: Size of chunks in characters (from config)
            chunk_overlap: Overlap between chunks in characters (from config)
        """
        logger.info(f"Initializing DocumentLoader with directory: {docs_dir}")
        self.docs_dir = Path(docs_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        logger.info(f"Document directory set to: {self.docs_dir}")
        logger.info(f"Chunking parameters - size: {chunk_size}, overlap: {chunk_overlap}")
        
    def load_documents(self) -> List[Dict]:
        """Load and parse all markdown files in directory.
        
        Returns:
            List[Dict]: List of documents with keys: 'content', 'metadata'
        """
        logger.info(f"Loading markdown documents from {self.docs_dir}")
        documents = []
        try:
            md_files = list(self.docs_dir.glob('*.md'))
            if not md_files:
                logger.warning(f"No markdown files found in {self.docs_dir}")
                return documents
                
            logger.info(f"Found {len(md_files)} markdown files")
            
            for md_file in md_files:
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if not content.strip():
                            logger.warning(f"Empty file: {md_file}")
                            continue
                            
                        documents.append({
                            'content': content,
                            'metadata': {
                                'source': str(md_file),
                                'file_name': md_file.name
                            }
                        })
                except Exception as e:
                    logger.error(f"Failed to read {md_file}: {e}")
                    
            if not documents:
                logger.error("No valid documents loaded")
            return documents
        except Exception as e:
            logger.error(f"Document loading failed: {e}")
            raise
        
    def watch_documents(self, callback: Callable[[Path], None]):
        """Start watching the docs directory for new/changed markdown files.
        
        Args:
            callback: Function to call when a new/changed .md file is detected
        """
        if not WATCHDOG_AVAILABLE:
            logger.warning("Cannot watch documents - watchdog package not installed")
            return
            
        if not self.docs_dir.exists():
            logger.error(f"Cannot watch non-existent directory: {self.docs_dir}")
            return
            
        try:
            event_handler = MarkdownFileHandler(callback)
            self.observer = Observer()
            self.observer.schedule(event_handler, str(self.docs_dir), recursive=True)
            self.observer.start()
            logger.info(f"Started watching {self.docs_dir} for markdown file changes")
        except Exception as e:
            logger.error(f"Failed to start document watcher: {e}")
        
    def stop_watching(self):
        """Stop watching the documents directory."""
        if self.observer and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logger.info("Stopped watching documents directory")

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Split documents into smaller chunks for processing.
        
        Args:
            documents: List of documents from load_documents()
            
        Returns:
            List[Dict]: List of chunks with same structure as input
        """
        if not documents:
            logger.error("No documents provided for chunking")
            return []
            
        logger.info(f"Chunking {len(documents)} documents")
        chunks = []
        # Validate chunking parameters
        if self.chunk_overlap >= self.chunk_size:
            logger.warning(f"Overlap {self.chunk_overlap} >= chunk_size {self.chunk_size}, reducing overlap to 25% of chunk_size")
            self.chunk_overlap = self.chunk_size // 4
        total_chars = sum(len(d['content']) for d in documents)
        logger.info(f"Total characters to process: {total_chars} with chunk_size={self.chunk_size}, overlap={self.chunk_overlap}")
        
        try:
            for doc in documents:
                
                content = doc['content']
                metadata = doc['metadata']
                
                start = 0
                prev_start = -1
                while start < len(content):
                    if start <= prev_start:
                        logger.error(f"Infinite loop detected at position {start} in document {metadata['file_name']}")
                        break
                    prev_start = start
                    
                    end = min(start + self.chunk_size, len(content))
                    chunk = content[start:end]
                    chunks.append(self._create_chunk(chunk, metadata, start, end))
                    
                    # Ensure we make forward progress
                    new_start = end - self.chunk_overlap
                    start = max(new_start, start + 1)  # Always move forward by at least 1
                    
                    logger.debug(f"Processed chunk {len(chunks)}: {start}-{end} of {len(content)} chars")
                    
            logger.debug(f"Created {len(chunks)} chunks from {len(documents)} documents")
            return chunks
            
        except Exception as e:
            logger.error(f"Chunking failed for document with metadata {doc.get('metadata', {})}: {e}")
            raise

    def _create_chunk(self, content: str, metadata: Dict, start: int, end: int) -> Dict:
        """Helper method to create a chunk dictionary.
        
        Args:
            content: The content of the chunk.
            metadata: Metadata of the original document.
            start: Start index of the chunk.
            end: End index of the chunk.
            
        Returns:
            Dict: A dictionary representing the chunk.
        """
        return {
            'content': content,
            'metadata': {
                **metadata,
                'chunk_start': start,
                'chunk_end': end
            }
        }
