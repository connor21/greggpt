"""Module to manage local LLM models."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)
from llama_cpp import Llama

class ModelManager:
    """Handles loading and querying of local LLM models."""
    
    def __init__(self, model_path: str):
        """Initialize with path to model files."""
        self.model_path = model_path
        self.llm = None
        
    def load_model(self):
        """Load the model into memory."""
        logger.info(f"Loading model from {self.model_path}")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=2048,
            n_threads=4
        )
        logger.info("Model loaded successfully")
        
    def generate_response(self, prompt: str) -> str:
        """Generate response from the model."""
        if not self.llm:
            raise RuntimeError("Model not loaded - call load_model() first")
            
        logger.info(f"Generating response for prompt (length: {len(prompt)} chars)")
        output = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7
        )
        response = output['choices'][0]['message']['content']
        logger.info(f"Generated response (length: {len(response)} chars)")
        return response
