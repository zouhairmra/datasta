import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

st.title("Economics Chatbot")

# Load docs from a folder
docs = SimpleDirectoryReader("data/pdfs").load_data()

# Build index
index = VectorStoreIndex.from_documents(docs)

# Query engine
query_engine = index.as_query_engine()

# User input
question = st.text_input("Ask a question about your economics PDFs:")

if question:
    response = query_engine.query(question)
    st.write(response)
