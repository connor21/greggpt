"""Module to manage local LLM models."""
from typing import Optional
from llama_cpp import Llama

class ModelManager:
    """Handles loading and querying of local LLM models."""
    
    def __init__(self, model_path: str):
        """Initialize with path to model files."""
        self.model_path = model_path
        self.llm = None
        
    def load_model(self):
        """Load the model into memory."""
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=2048,
            n_threads=4
        )
        
    def generate_response(self, prompt: str) -> str:
        """Generate response from the model."""
        if not self.llm:
            raise RuntimeError("Model not loaded - call load_model() first")
            
        output = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7
        )
        return output['choices'][0]['message']['content']
