import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

PDF_DIR = "data/pdfs"

if not os.path.exists(PDF_DIR):
    st.error(f"📁 Directory `{PDF_DIR}` not found. Please upload your PDF files to that folder.")
else:
    docs = SimpleDirectoryReader(PDF_DIR).load_data()
    index = VectorStoreIndex.from_documents(docs)
    query_engine = index.as_query_engine()

    st.title("📚 Economic Chatbot")

    query = st.text_input("Ask a question about the uploaded documents:")

    if query:
        response = query_engine.query(query)
        st.write(response)
