"""Module to manage local LLM models."""
import logging
import os
import torch
from typing import Dict, Optional, Tuple
import yaml

logger = logging.getLogger(__name__)
from llama_cpp import Llama
from transformers import AutoModelForCausalLM, AutoTokenizer

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
        self.hardware_info = self._get_hardware_info()
        
    def _get_hardware_info(self) -> Dict:
        """Get information about available hardware."""
        gpu_available = torch.cuda.is_available()
        return {
            'gpu_available': gpu_available,
            'gpu_count': torch.cuda.device_count() if gpu_available else 0,
            'gpu_name': torch.cuda.get_device_name(0) if gpu_available else None,
            'cpu_cores': os.cpu_count()
        }
        
    def load_model(self, model_name: Optional[str] = None):
        """Load the specified model into memory."""
        model_name = model_name or self.active_model
        model_config = self.models.get(model_name)
        
        if not model_config:
            raise ValueError(f"Model {model_name} not found in config")
            
        model_path = model_config['path']
        logger.info(f"Loading model {model_name} from {model_path}")
        
        # Determine model type based on file extension
        hardware_config = self.config.get('hardware', {})
        use_gpu = hardware_config.get('enable_gpu', False) and self.hardware_info['gpu_available']
        
        if model_path.endswith('.gguf'):
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=4
            )
        elif model_path.endswith('.safetensors'):
            device = 'cuda' if use_gpu else 'cpu'
            logger.info(f"Loading model on {device.upper()}")
            self.llm = {
                'model': AutoModelForCausalLM.from_pretrained(
                    model_path,
                    device_map='auto' if use_gpu else None,
                    torch_dtype=torch.float16 if use_gpu else torch.float32
                ),
                'tokenizer': AutoTokenizer.from_pretrained(model_path)
            }
        else:
            raise ValueError(f"Unsupported model format: {model_path}")
            
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
        
        if isinstance(self.llm, dict):  # Transformers model
            inputs = self.llm['tokenizer'](prompt, return_tensors="pt")
            outputs = self.llm['model'].generate(
                **inputs,
                max_new_tokens=model_config.get('max_tokens', 512),
                temperature=model_config.get('temperature', 0.7),
                top_p=model_config.get('top_p', 0.9)
            )
            response = self.llm['tokenizer'].decode(outputs[0], skip_special_tokens=True)
        else:  # GGUF model
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
        
    def get_hardware_info(self) -> Dict:
        """Get information about available hardware."""
        return self.hardware_info
