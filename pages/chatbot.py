import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import ContextChatEngine

import os
import tempfile

st.set_page_config(page_title="📚📤 PDF Chatbot", layout="wide")
st.title("🤖💬 Ask Questions from Your PDF (No API Key Needed)")

uploaded_files = st.file_uploader("📄 Upload PDF file(s)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("🔄 Processing uploaded PDFs..."):

        # Create temporary directory to store uploaded PDFs
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_files:
                with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.read())

            # Load documents from temp directory
            docs = SimpleDirectoryReader(temp_dir).load_data()

        # Set up local model (make sure Ollama is running locally)
        llm
