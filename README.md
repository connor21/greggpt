# greggpt

A local document-based chatbot with Streamlit interface.

## Features
- Chat with your local documents using local LLMs
- Private and secure - no data leaves your machine
- Supports markdown documents
- Simple web interface

## Setup
1. Create virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your markdown documents in `docs/` directory

## Usage
Run the Streamlit app:
```bash
streamlit run src/main.py
```

## Configuration
Edit `config.yaml` to customize:
- Model paths
- Document processing settings
- Retrieval parameters
