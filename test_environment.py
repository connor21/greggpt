"""Test environment for gregGPT components."""
from src.models.model_manager import ModelManager

def test_model_setup():
    """Test model loading and basic response generation."""
    print("Testing model setup...")
    
    model_path = "/Volumes/SafeSpace/getNext-IT/__workdir__/greggpt/models/tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    manager = ModelManager(model_path)
    
    print("Loading model...")
    manager.load_model()
    
    print("Testing prompt response...")
    response = manager.generate_response("Hello, how are you?")
    print(f"Model response: {response}")
    
    print("Model setup test completed successfully")

if __name__ == "__main__":
    test_model_setup()
