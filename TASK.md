# TASK.md

This checklist outlines the modular, independent steps required to build and deploy **gregGPT**, a local document-based chatbot with a Streamlit interface. Each task can be performed independently and tracked for progress.

---

## ✅ Environment Setup
- [x] Create Python 3.12 virtual environment
- [x] Generate `requirements.txt` and freeze dependencies
- [x] Validate dependency installation via test script

## ✅ Project Initialization
- [x] Create folder structure and placeholder files as in `PLANNING.md`
- [x] Set up `.gitignore`, `README.md`, and repo initialization

## ✅ Model Setup
- [x] Choose and download local LLM model (e.g. llama.cpp, GPT4All)
- [x] Store model in `models/`
- [x] Implement `model_manager.py` to load and query model
- [x] Test LLM with basic prompt/response

## ✅ Document Ingestion
- [ ] Implement Markdown loader in `document_loader.py`
- [ ] Chunk and clean `.md` text data
- [ ] Generate embeddings and store in `vectorstore/`

## ✅ Embedding and Vector Store
- [ ] Select and initialize vector store (FAISS or Chroma)
- [ ] Implement storage, retrieval, and query interfaces
- [ ] Validate stored documents and retrieval relevance

## ✅ RAG Pipeline
- [ ] Implement `retriever.py` to fetch relevant context
- [ ] Assemble prompt using retrieved context + user query
- [ ] Add filtering logic for irrelevant matches

## ✅ Chat Logic
- [ ] Create `chat_handler.py` with message-passing interface
- [ ] Integrate model, retriever, and prompt composer
- [ ] Format output and track source citations

## ✅ Streamlit Interface
- [ ] Build chat UI in `main.py` with input and response blocks
- [ ] Add session state, reset, and timestamp features
- [ ] Display token usage and document matches (optional)

## ✅ Configuration
- [ ] Create `config.yaml` with paths, chunk sizes, model params
- [ ] Implement config loader and error fallback logic

## ✅ Logging and Testing
- [ ] Add `logging` to all modules
- [ ] Write unit tests using `pytest` for core functions
- [ ] Create test Markdown file and sample queries

## ✅ Cleanup and Optimization
- [ ] Optimize chunking and embedding performance
- [ ] Clean up unused imports, functions, and test artifacts
- [ ] Add error handling for empty queries, missing models, etc.

## ✅ Documentation and Deployment
- [ ] Expand `README.md` with setup, usage, and design notes
- [ ] Add usage examples and screenshots to README
- [ ] Create `Dockerfile` and test container build locally

## ✅ Optional Features
- [ ] UI toggle to switch between multiple models
- [ ] Watch folder for new `.md` documents
- [ ] Enable memory / con
