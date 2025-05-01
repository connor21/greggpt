"""Configuration loader with error fallback logic."""
from pathlib import Path
import yaml
from typing import Any, Dict
from pydantic import BaseModel, ValidationError

class ConfigModel(BaseModel):
    """Pydantic model for configuration validation."""
    model_path: str
    docs_dir: str
    vectorstore_path: str
    max_tokens: int
    temperature: float
    top_p: float
    chunk_size: int
    chunk_overlap: int

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load and validate configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValidationError: If config validation fails
    """
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    try:
        validated = ConfigModel(**config).dict()
        return validated
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}")

def get_config_with_fallback(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load config with graceful fallback to defaults on error.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary (validated or fallback defaults)
    """
    fallback_config = {
        "model_path": "models/default.gguf",
        "docs_dir": "documents",
        "vectorstore_path": "vectorstore",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "chunk_size": 1000,
        "chunk_overlap": 200
    }
    
    try:
        return load_config(config_path)
    except Exception as e:
        print(f"Using fallback config due to error: {e}")
        return fallback_config
