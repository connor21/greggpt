"""Main Streamlit application for greggpt."""
import logging
import sys
from pathlib import Path
import streamlit as st
from datetime import datetime

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

def main():
    """Main application interface."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    st.title("greggpt - Document Chat Interface")
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
    main()
