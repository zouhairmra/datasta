# pages/chatbot.py
import streamlit as st
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.llms.ollama import Ollama
import os

st.set_page_config(page_title="📘 AI Economics Chatbot", page_icon="🤖")
st.title("📘 Ask Me Anything: Economics Edition")

# Load or create index from PDFs
@st.cache_resource(show_spinner=True)
def load_index():
    documents = SimpleDirectoryReader("pdf_data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index

# Initialize LLM and query engine
index = load_index()
llm = Ollama(model="llama3")
query_engine = index.as_query_engine(llm=llm)

# Chat UI
query = st.text_input("Ask your question (in English or Arabic):")

if query:
    with st.spinner("Thinking..."):
        response = query_engine.query(query)
        st.markdown(f"### 🤖 Answer:\n{response.response}")

# File upload to enhance PDF corpus
st.sidebar.header("📁 Add Your Own PDFs")
uploaded_files = st.sidebar.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    os.makedirs("pdf_data", exist_ok=True)
    for file in uploaded_files:
        with open(f"pdf_data/{file.name}", "wb") as f:
            f.write(file.read())
    st.sidebar.success("Uploaded! Please refresh the page to include new PDFs.")

st.sidebar.info("This assistant uses local LLMs and retrieval-based QA to answer your economics questions.")
