"""Module to manage local LLM models."""
import logging
from typing import Dict, Optional
import yaml

logger = logging.getLogger(__name__)
from llama_cpp import Llama

class ModelManager:
    """Handles loading and querying of local LLM models."""
    
    def __init__(self, config: Dict):
        """Initialize with configuration dictionary."""
        self.config = config
        self.models = config.get('models', {
            'default': {
                'path': config.get('model_path'),
                'max_tokens': config.get('max_tokens', 512),
                'temperature': config.get('temperature', 0.7),
                'top_p': config.get('top_p', 0.9)
            }
        })
        self.active_model = config.get('active_model', 'default')
        self.llm = None
        
    def load_model(self, model_name: Optional[str] = None):
        """Load the specified model into memory."""
        model_name = model_name or self.active_model
        model_config = self.models.get(model_name)
        
        if not model_config:
            raise ValueError(f"Model {model_name} not found in config")
            
        logger.info(f"Loading model {model_name} from {model_config['path']}")
        self.llm = Llama(
            model_path=model_config['path'],
            n_ctx=2048,
            n_threads=4
        )
        self.active_model = model_name
        logger.info(f"Model {model_name} loaded successfully")
        
    def switch_model(self, model_name: str):
        """Switch to a different model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available")
        if model_name != self.active_model:
            self.load_model(model_name)
            
    def generate_response(self, prompt: str) -> str:
        """Generate response from the active model."""
        if not self.llm:
            raise RuntimeError("Model not loaded - call load_model() first")
            
        model_config = self.models[self.active_model]
        logger.info(f"Generating response using {self.active_model} model")
        
        output = self.llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=model_config.get('max_tokens', 512),
            temperature=model_config.get('temperature', 0.7),
            top_p=model_config.get('top_p', 0.9)
        )
        response = output['choices'][0]['message']['content']
        logger.info(f"Generated response (length: {len(response)} chars)")
        return response
        
    def get_available_models(self) -> Dict:
        """Return dictionary of available models."""
        return {name: cfg['path'] for name, cfg in self.models.items()}
