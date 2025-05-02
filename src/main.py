"""Main Streamlit application for greggpt."""
import asyncio
import logging
import sys
from pathlib import Path
import streamlit as st
from datetime import datetime

# Initialize event loop before anything else
import asyncio
import nest_asyncio
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
nest_asyncio.apply()

# Configure Streamlit to avoid PyTorch conflicts
import streamlit as st
import os
os.environ['STREAMLIT_SERVER_ENABLE_FILE_WATCHER'] = 'false'

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from chat_handler import ChatHandler
import yaml

def load_config():
    """Load configuration from file."""
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def init_chat_handler():
    """Initialize and cache the ChatHandler."""
    config = load_config()
    return ChatHandler(config)

def cleanup_resources():
    """Clean up multiprocessing resources."""
    import multiprocessing
    import multiprocessing.util
    if multiprocessing.current_process().name == 'MainProcess':
        # Force cleanup of all resources
        multiprocessing.util._cleanup()
        # Close all active pools and managers
        for pool in multiprocessing.active_children():
            pool.terminate()
        # Explicitly clean up semaphores
        if hasattr(multiprocessing, '_semaphore_tracker'):
            multiprocessing._semaphore_tracker._stop()

def main():
    """Main application interface."""
    import atexit
    atexit.register(cleanup_resources)
    
    # File watching already disabled via environment variable
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    st.title("GREGgpt - Document Chat Interface")
    st.write("Chat with your documents using local LLMs")
    
    # Initialize chat handler
    chat_handler = init_chat_handler()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.token_count = 0
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                st.caption(f"Sources: {', '.join(s['source'] for s in msg['sources'])}")
            if msg.get("timestamp"):
                st.caption(msg["timestamp"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents"):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        # Process query and get response
        result = chat_handler.process_query(prompt)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "sources": result["sources"],
            "tokens": result["tokens"],
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.token_count += result["tokens"]
        
        # Rerun to display new messages
        st.rerun()
    
    # Sidebar with stats and controls
    with st.sidebar:
        st.header("Session Info")
        st.metric("Total Tokens Used", st.session_state.token_count)
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.token_count = 0
            st.rerun()

if __name__ == "__main__":
    # Isolate PyTorch from Streamlit
    import os
    os.environ['STREAMLIT_SERVER_ENABLE_FILE_WATCHER'] = 'false'
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
    
    try:
        main()
    finally:
        # Safer resource cleanup
        import multiprocessing
        for p in multiprocessing.active_children():
            try:
                p.terminate()
                p.join()
            except:
                pass
