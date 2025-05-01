# PLANNING.md

## Project: gregGPT

**gregGPT** is a locally running AI chatbot built with open-source language models. It includes a Streamlit-based user interface and supports retrieval-augmented generation (RAG) using Markdown files as knowledge sources. It aims to provide a fast, private, and extendable conversational interface that respects data sovereignty.

---

## Goals

- Run an LLM locally without relying on cloud APIs
- Provide a web-based chat interface using Streamlit
- Allow knowledge injection via Markdown documents
- Enable modular, maintainable, and well-documented Python code
- Ensure reproducibility via environment management and dependency tracking

---

## Components

1. **LLM Engine**
   - A local language model (e.g., `llama.cpp`, `GPT4All`, `Mistral`, `phi2`)
   - Model loaded via `llama-cpp-python`, `transformers`, or `llm` frameworks

2. **RAG (Retrieval-Augmented Generation) Layer**
   - Document ingestion and vectorization (`LangChain`, `Chroma`, `FAISS`)
   - Document retriever and prompt composer

3. **Chat Interface**
   - Streamlit front-end for real-time chat
   - Conversation history, metadata display, reset options

4. **Markdown Loader**
   - Extract content from `.md` files
   - Embed and store vectors in local database

5. **Backend Core**
   - Controller logic: model loading, query processing
   - Utilities for logging, config loading, error handling

---

## Development Environment

- Python 3.10+
- OS: Linux/macOS/Windows
- Virtual environment via `venv` or `conda`
- Optional GPU support (CUDA or Metal for acceleration)

---

## File Structure

```
gregGPT/
├── app/
│   ├── main.py               # Streamlit UI entry point
│   ├── chat_handler.py       # Handles user messages and model responses
│   ├── document_loader.py    # Ingests and vectorizes markdown files
│   ├── model_manager.py      # Loads and interfaces with the LLM
│   ├── retriever.py          # Similarity search from document vectors
│   └── utils.py              # Helper functions and logging
│
├── data/
│   ├── documents/            # User-supplied markdown files
│   └── vectorstore/          # Stored vector indexes
│
├── models/                   # Folder to store downloaded models
│
├── requirements.txt
├── README.md
└── PLANNING.md               # This file
```

---

## Style Guide

- **Formatting**: Follow [PEP8](https://peps.python.org/pep-0008/)
- **Naming Conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - Constants in `UPPER_SNAKE_CASE`
- **Comments and Docstrings**:
  - Use Google-style docstrings
  - Provide inline comments only when necessary
- **Type Annotations**: Use typing for all function inputs and outputs
- **Modularity**: Functions should do one thing and be testable

---

## Dependencies

```txt
streamlit
langchain
llama-cpp-python
faiss-cpu                # or faiss-gpu
sentence-transformers
pandas
tqdm
PyYAML
```

Optional for model support:
```txt
transformers
accelerate
torch
```

---

## Optional Additions

### Configuration Support

Create a `config.yaml` to manage model paths, chunk size, etc.

### Tests

Add a `tests/` folder with `pytest` for core modules.

### Docker Support

Consider including a `Dockerfile` and `.devcontainer` setup for isolated dev environments.

---

## Future Extensions

- Add chat memory for multi-turn context
- Multi-file document ingestion with folder watching
- Role-based prompting
- Support for different embedding models
- Switchable models via UI

---

## Status

- ☑ Base chatbot working
- ☑ Streamlit UI operational
- ☑ Markdown RAG functional
- ☑ Modular structure with type hints
- ☑ Test coverage for critical modules

