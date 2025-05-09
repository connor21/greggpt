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
- [x] Implement Markdown loader in `document_loader.py`
- [x] Chunk and clean `.md` text data
- [x] Generate embeddings and store in `vectorstore/`

## ✅ Embedding and Vector Store
- [x] Select and initialize vector store (Chroma)
- [x] Implement storage, retrieval, and query interfaces
- [x] Validate stored documents and retrieval relevance (test_vectorstore.py)

## ✅ RAG Pipeline
- [x] Implement `retriever.py` to fetch relevant context
- [x] Assemble prompt using retrieved context + user query
- [x] Add filtering logic for irrelevant matches (distance threshold)

## ✅ Chat Logic
- [x] Create `chat_handler.py` with message-passing interface
- [x] Integrate model, retriever, and prompt composer
- [x] Format output and track source citations (test_chat_handler.py)

## ✅ Streamlit Interface
- [x] Build chat UI in `main.py` with input and response blocks
- [x] Add session state, reset, and timestamp features
- [x] Display token usage and document matches

## ✅ Configuration
- [x] Create `config.yaml` with paths, chunk sizes, model params
- [x] Implement config loader and error fallback logic

## ✅ Logging and Testing
- [x] Add `logging` to all modules
- [x] Write unit tests using `pytest` for core functions
- [x] Create test Markdown file and sample queries

## ✅ Cleanup and Optimization
- [x] Fix document loading at startup in RAG pipeline
- [x] Optimize chunking and embedding performance
- [x] Clean up unused imports, functions, and test artifacts
- [x] Add error handling for empty queries, missing models, etc.
- [x] Only process documents on startup or if the AI model is changed (5/6/2025)

## ✅ Documentation and Deployment
- [x] Expand `README.md` with setup, usage, and design notes
- [x] Add usage examples and screenshots to README
- [x] Create `Dockerfile` and test container build locally

## ✅ Optional Features
- [x] UI toggle to switch between multiple models
- [x] Improve citation formatting for gregGPT responses
- [x] Watch folder for new `.md` documents (5/9/2025)
- [x] Add a parameter to `config.yaml` to set the log level used for logging (5/9/2025)

## ✅ Design the Citation Format
- [x] Should strip raw metadata (e.g., `chunk_start`, `distance`)
- [x] Display only: Cleaned file name (e.g., `Agile Project Management`), optionally a preview or section title
- [x] Decide if Markdown, footnotes, or bullet lists will be used based on front-end rendering capabilities
- [x] Modify the response builder in the backend to apply new formatting logic
- [x] Create a formatting utility function (e.g., `format_sources(results)` in Python or JS)
- [x] Output: Clean, user-facing string or HTML
- [x] Remove technical metadata from user-facing output (`chunk_start`, `distance`, etc.)
- [x] Add the new `Sources:` section to the final response payload
- [x] Ensure that the front-end renders the new citation format correctly
- [x] Markdown rendering, styled list, or tooltip format
- [x] Write unit tests for the formatting function
- [x] Verify no breaking changes to current app behavior

## ✅ Add GPU Support
- [x] If GPU available use it for processing queries (5/9/2025)
- [x] Make usage of GPU configurable in `config.yaml` (5/9/2025)
- [x] Add GPU and CPU hardware information in sidebar of app (5/9/2025)

