# greggpt

A local document-based chatbot with Streamlit interface that uses Retrieval-Augmented Generation (RAG) with local LLMs.

## Features
- Chat with your local documents using local LLMs (llama.cpp, GPT4All, etc.)
- Private and secure - no data leaves your machine
- Supports markdown documents
- Simple web interface with conversation history
- Document source citations
- Token usage tracking

## Architecture Overview
![System Architecture](docs/architecture.png)

greggpt follows a modular RAG pipeline:
1. **Document Ingestion**: Markdown files are loaded, chunked and embedded
2. **Vector Store**: ChromaDB stores document embeddings for retrieval
3. **Retriever**: Finds relevant document chunks for queries
4. **LLM**: Local model generates responses using retrieved context
5. **Interface**: Streamlit web app for user interaction

## Setup

### Prerequisites
- Python 3.12
- 8GB+ RAM (for local LLMs)
- 4GB+ disk space for models

### Installation
1. Create virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download a local LLM (e.g. TinyLlama) and place in `models/`:
```bash
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf -P models/
```

4. Place your markdown documents in `docs/` directory

## Usage

### Running the App
```bash
streamlit run src/main.py
```

The web interface will open at http://localhost:8501

### Example Queries
1. "What are the key points from the documentation?"
2. "Summarize the installation instructions"
3. "Explain how the vector store works"

![Screenshot](docs/screenshot.png)

## Configuration
Edit `config.yaml` to customize:

```yaml
# Model settings
model_path: "models/tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
max_tokens: 512
temperature: 0.7

# Document processing
chunk_size: 1000  # characters
chunk_overlap: 200

# Paths
docs_dir: "docs"
vectorstore_path: "vectorstore"
```

## Docker Deployment
Build and run the container:
```bash
docker build -t greggpt .
docker run -p 8501:8501 greggpt
```

## Troubleshooting
- **Model not loading**: Verify model file exists at configured path
- **No documents found**: Check docs directory in config.yaml
- **Performance issues**: Reduce chunk_size or use smaller model

## Development
To contribute:
1. Fork the repository
2. Create feature branch
3. Submit pull request

Run tests:
```bash
pytest tests/
