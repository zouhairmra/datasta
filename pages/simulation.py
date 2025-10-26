# app.py (UPDATED — Integrated Course FAQ Chatbot)
import streamlit as st
import requests
import json
import time
import pandas as pd
import io
from pathlib import Path

# --- Optional/soft imports (handle if missing) ---
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

# LangChain + embeddings + FAISS
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
    LC_AVAILABLE = True
except Exception:
    LC_AVAILABLE = False

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask anything about economics, econometrics, or data analysis — or upload a file for AI insights.")

# ==========================
# POE API CONFIG (original chat)
# ==========================
POE_API_URL = "https://api.poe.com/v1/chat/completions"
POE_API_KEY = st.secrets.get("POE_API_KEY", "YOUR_POE_API_KEY_HERE")
MODEL = st.selectbox("Select model", ["maztouriabot", "gpt-4o-mini", "claude-3-haiku"])

# ==========================
# STATE INIT
# ==========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "faq_index" not in st.session_state:
    st.session_state["faq_index"] = None  # will hold FAISS index object
if "faq_docs_meta" not in st.session_state:
    st.session_state["faq_docs_meta"] = []  # metadata for docs uploaded for FAQ

# ==========================
# FILE UPLOAD (course docs + data)
# ==========================
st.markdown("### 📂 Upload a file for AI analysis")
uploaded_file = st.file_uploader("Upload PDF, CSV, DOCX, or TXT", type=["pdf", "csv", "docx", "txt"], accept_multiple_files=False)
uploaded_text = ""
df = None

def safe_read_csv(uploaded_file_obj):
    # handle different encodings and return a DataFrame or raise
    try:
        uploaded_file_obj.seek(0)
        return pd.read_csv(uploaded_file_obj, encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            uploaded_file_obj.seek(0)
            return pd.read_csv(uploaded_file_obj, encoding="latin1")
        except Exception as e:
            raise e
    except Exception as e:
        raise e

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()

    # PDF
    if file_ext == "pdf":
        if PdfReader:
            try:
                uploaded_file.seek(0)
                reader = PdfReader(uploaded_file)
                text_pages = []
                for p in reader.pages:
                    text_pages.append(p.extract_text() or "")
                uploaded_text = "\n\n".join(text_pages)
                st.success("✅ PDF text extracted.")
            except Exception as e:
                st.error(f"❌ PDF extraction failed: {e}")
        else:
            # fallback try langchain loader if available
            if LC_AVAILABLE:
                try:
                    uploaded_file.seek(0)
                    tmp_path = Path("tmp_uploaded.pdf")
                    with open(tmp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    loader = PyPDFLoader(str(tmp_path))
                    docs = loader.load()
                    uploaded_text = "\n\n".join([d.page_content for d in docs])
                    tmp_path.unlink(missing_ok=True)
                    st.success("✅ PDF text extracted via LangChain loader.")
                except Exception as e:
                    st.error(f"❌ PDF extraction failed (langchain): {e}")
            else:
                st.error("PyPDF2 not installed; cannot extract PDF text.")

    # Word
    elif file_ext == "docx":
        if Document:
            try:
                uploaded_file.seek(0)
                doc = Document(uploaded_file)
                uploaded_text = "\n".join([p.text for p in doc.paragraphs])
                st.success("✅ Word text extracted.")
            except Exception as e:
                st.error(f"❌ DOCX extraction failed: {e}")
        else:
            # try langchain loader fallback
            if LC_AVAILABLE:
                try:
                    uploaded_file.seek(0)
                    tmp_path = Path("tmp_uploaded.docx")
                    with open(tmp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    loader = UnstructuredWordDocumentLoader(str(tmp_path))
                    docs = loader.load()
                    uploaded_text = "\n\n".join([d.page_content for d in docs])
                    tmp_path.unlink(missing_ok=True)
                    st.success("✅ DOCX text extracted via LangChain loader.")
                except Exception as e:
                    st.error(f"❌ DOCX extraction failed (langchain): {e}")
            else:
                st.error("python-docx not installed; cannot extract DOCX text.")

    # TXT
    elif file_ext == "txt":
        try:
            uploaded_file.seek(0)
            uploaded_text = uploaded_file.read().decode("utf-8", errors="ignore")
            st.success("✅ TXT file read.")
        except Exception as e:
            st.error(f"❌ TXT read failed: {e}")

    # CSV
    elif file_ext == "csv":
        try:
            uploaded_file.seek(0)
            df = safe_read_csv(uploaded_file)
            st.dataframe(df.head())
            uploaded_text = df.to_string(index=False)
            st.success("✅ CSV data loaded with proper encoding.")
        except Exception as e:
            st.error(f"❌ Could not read CSV file: {e}")
            df = None
            uploaded_text = ""

    with st.expander("📜 Preview Extracted Text"):
        st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

# ==========================
# DATA ANALYSIS TOOLS (keep original behavior)
# ==========================
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except Exception:
    sns = None

try:
    import statsmodels.api as sm
except Exception:
    sm = None

if df is not None:
    st.markdown("### 📊 Data Analysis Tools")

    if st.button("Plot Pairplot (Seaborn)"):
        if sns:
            st.write("Generating pairplot...")
            fig = sns.pairplot(df.select_dtypes(include="number"))
            st.pyplot(fig)
        else:
            st.warning("⚠️ seaborn not installed. Cannot generate pairplot.")

    if sm and st.button("Run OLS Regression (Statsmodels)"):
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) >= 2:
            y_col = st.selectbox("Select dependent variable", numeric_cols, key="ycol")
            X_cols = st.multiselect("Select independent variables", [c for c in numeric_cols if c != y_col], key="xcols")
            if X_cols:
                X = sm.add_constant(df[X_cols])
                y = df[y_col]
                model = sm.OLS(y, X).fit()
                st.write(model.summary())
        else:
            st.warning("Not enough numeric columns for regression.")

# ==========================
# COURSE FAQ CHATBOT SECTION (NEW)
# ==========================
st.markdown("---")
st.header("📚 Course FAQ Chatbot (RAG-backed)")

st.markdown("""
Use this mode to upload your course documents (syllabus, assignment sheets, policies).  
The FAQ bot will answer questions using ONLY the uploaded documents and will cite sources.  
If the info is not present, it will reply: *"I don't know — please ask the instructor."*
""")

# Course selection and language options
course_choice = st.selectbox("Choose course to power the FAQ bot", [
    "Business Mathematics II (Bilingual: EN + AR)",
    "Principles of Microeconomics (Arabic: MSA + light Qatari tone)"
])

faq_enable = st.checkbox("Enable Course FAQ Mode", value=False)

# Ingest documents for FAQ (separate upload area)
st.markdown("**Upload course documents for the FAQ bot (PDF / DOCX / TXT).**")
faq_files = st.file_uploader("Upload course docs for FAQ (you can upload one file at a time)", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="faq_upload")

faq_index_folder = "faq_faiss_index"  # local folder to save index for persistence (if desired)
faq_embed_model = "text-embedding-3-small"  # or change as needed

def build_faq_index_from_files(files):
    """Load uploaded files, split, embed, and build FAISS index in session_state."""
    if not LC_AVAILABLE:
        st.error("LangChain/embeddings not available in environment. Install langchain + openai + faiss-cpu to enable FAQ.")
        return None

    docs = []
    meta = []
    tmp_paths = []
    for f in files:
        name = f.name
        try:
            ext = name.split(".")[-1].lower()
            tmp = Path(f"tmp_faq_{name}")
            with open(tmp, "wb") as fh:
                fh.write(f.getbuffer())
            tmp_paths.append(tmp)

            if ext == "pdf":
                loader = PyPDFLoader(str(tmp))
                loaded = loader.load()
            elif ext in ["docx", "doc"]:
                loader = UnstructuredWordDocumentLoader(str(tmp))
                loaded = loader.load()
            elif ext == "txt":
                loader = TextLoader(str(tmp), encoding="utf8")
                loaded = loader.load()
            else:
                loaded = []
            # attach source metadata
            for d in loaded:
                d.metadata["source"] = name
            docs.extend(loaded)
            meta.append({"filename": name, "chunks": len(loaded)})
        except Exception as e:
            st.warning(f"Could not load {name}: {e}")

    if not docs:
        st.error("No documents loaded for FAQ index.")
        for p in tmp_paths:
            p.unlink(missing_ok=True)
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    split_docs = splitter.split_documents(docs)
    emb = OpenAIEmbeddings(model=faq_embed_model)
    vs = FAISS.from_documents(split_docs, emb)
    # save local copy if desired
    try:
        vs.save_local(faq_index_folder)
    except Exception:
        pass

    # cleanup temp files
    for p in tmp_paths:
        p.unlink(missing_ok=True)
    return vs, meta

if faq_files:
    if st.button("Index uploaded FAQ documents"):
        with st.spinner("Building FAQ index (this may take a moment)..."):
            res = build_faq_index_from_files(faq_files)
            if res:
                vs_obj, meta = res
                st.session_state["faq_index"] = vs_obj
                st.session_state["faq_docs_meta"] = meta
                st.success("✅ FAQ index built and loaded into memory.")
else:
    st.info("Upload course documents here and click 'Index uploaded FAQ documents' to build the FAQ knowledge base.")

# RAG prompt templates (language-aware)
RAG_BASE = """You are an assistant that answers student questions using ONLY the following CONTEXT extracted from course documents.
Rules:
- Use ONLY the context below. Do NOT use outside knowledge.
- If the answer cannot be found in the context, reply exactly: "I don't know — please ask the instructor."
- Provide a one-line source citation at the end in the format: [filename].
- Keep answers concise and student-friendly.

Context:
{context}

Question:
{question}

Answer:"""

RAG_BILINGUAL_SUFFIX = "\nIf the question is in Arabic, answer in Arabic; if it's in English, answer in English. Keep Arabic formal but friendly."

RAG_MSA_QATARI_SUFFIX = "\nAnswer in Modern Standard Arabic using a lightly Qatari-friendly tone. Keep answers professional and concise."

def run_faq_query(question: str, faiss_index, top_k=5, temp=0.0):
    if not faiss_index:
        return "FAQ knowledge base not loaded. Please upload and index course documents."
    retriever = faiss_index.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.get_relevant_documents(question)
    if not docs:
        return "I don't know — please ask the instructor."

    # Concatenate context but keep source markers
    context = "\n\n---\n\n".join([f"[{d.metadata.get('source','unknown')}]\n{d.page_content}" for d in docs])
    # choose suffix based on course
    if "Business Mathematics" in course_choice:
        prompt = RAG_BASE + RAG_BILINGUAL_SUFFIX
    else:
        prompt = RAG_BASE + RAG_MSA_QATARI_SUFFIX
    prompt_filled = prompt.format(context=context, question=question)

    # Call OpenAI completion (use OpenAI as an assistant for RAG)
    # You should set OPENAI_API_KEY in Streamlit secrets for embeddings/LLM calls
    OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", None)
    if not OPENAI_KEY:
        return "OpenAI API key not configured in Streamlit secrets. Cannot process FAQ queries."

    # Use OpenAI chat/completions via API
    import openai
    openai.api_key = OPENAI_KEY
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # change if you have another model available
            messages=[{"role": "user", "content": prompt_filled}],
            temperature=temp,
            max_tokens=500,
        )
        answer = resp["choices"][0]["message"]["content"].strip()
        # Safety: ensure the model didn't hallucinate beyond context by checking for keyword:
        if answer.lower().startswith("i don't know") or "please ask the instructor" in answer.lower():
            return "I don't know — please ask the instructor."
        # Append simple citations from the retrieved docs
        sources = list({d.metadata.get("source","unknown") for d in docs})
        cite_line = "\n\nSources: " + ", ".join(sources)
        return answer + cite_line
    except Exception as e:
        return f"Error when calling OpenAI for RAG: {e}"

# FAQ interaction UI
if faq_enable:
    st.markdown("**Course FAQ Mode is ON — questions will be answered from the indexed course documents.**")
    faq_question = st.text_input("Ask the course (FAQ bot):", placeholder="e.g., When is Assignment 2 due?")
    if st.button("Ask FAQ bot"):
        if not st.session_state.get("faq_index"):
            st.error("FAQ index not loaded. Upload and index course docs first.")
        elif not faq_question.strip():
            st.warning("Please type a question for the FAQ bot.")
        else:
            with st.spinner("Searching course documents..."):
                answer = run_faq_query(faq_question, st.session_state["faq_index"], top_k=5)
                st.markdown("**FAQ Bot answer:**")
                st.write(answer)

# ==========================
# MAIN CHAT (original POE API flow)
# ==========================
st.markdown("---")
st.header("💬 General AI Chat (POE API)")

# display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

default_prompt = "Summarize the uploaded document." if uploaded_text else ""
user_input = st.chat_input("Type your question or ask about your uploaded file...") or default_prompt

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            headers = {"Authorization": f"Bearer {POE_API_KEY}", "Content-Type": "application/json"}
            content = f"File content:\n{uploaded_text[:4000]}\n\nQuestion: {user_input}" if uploaded_text else user_input
            payload = {"model": MODEL, "messages": [{"role": "user", "content": content}]}

            res = requests.post(POE_API_URL, headers=headers, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            response_text = data["choices"][0]["message"]["content"]

            for token in response_text.split():
                full_response += token + " "
                placeholder.markdown(full_response + "▌")
                time.sleep(0.03)
            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error fetching response: {e}")
            full_response = f"Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# ==========================
# EXPORT CHAT
# ==========================
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 2])

if col1.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared!")

if col2.button("💾 Export Chat"):
    if st.session_state["messages"]:
        chat_data = pd.DataFrame(st.session_state["messages"])
        st.download_button("Download CSV", chat_data.to_csv(index=False), "econlab_chat.csv", "text/csv")
    else:
        st.warning("No chat to export!")

st.markdown("---")
st.caption("💡 EconLab AI Assistant — FAQ Bot integrated. RAG uses OpenAI for embeddings & LLM. Configure OPENAI_API_KEY in Streamlit secrets.")
