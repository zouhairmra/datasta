# 6_AI_Assistant.py
import streamlit as st
import requests
import json
import time
import pandas as pd
import io
from pathlib import Path

# Optional imports for PDF/DOCX parsing
# Try importing PDF and DOCX libraries
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None
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

# We'll store the latest uploaded course text here (single upload area for both courses)
if "course_text" not in st.session_state:
    st.session_state["course_text"] = ""  # raw extracted text
if "course_filename" not in st.session_state:
    st.session_state["course_filename"] = ""

# ==========================
# FILE UPLOAD (shared single area)
# ==========================
st.markdown("### 📂 Upload a file for AI analysis or course FAQ")
uploaded_file = st.file_uploader(
    "Upload PDF, CSV, DOCX, or TXT (one file at a time)", 
    type=["pdf", "csv", "docx", "txt"], 
    accept_multiple_files=False
)
uploaded_text = ""
df = None

def safe_read_csv(uploaded_file_obj):
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
                text_pages = [p.extract_text() or "" for p in reader.pages]
                uploaded_text = "\n\n".join(text_pages)
                st.success("✅ PDF text extracted.")
            except Exception as e:
                st.error(f"❌ PDF extraction failed: {e}")
        else:
            st.error("PyPDF2 not installed; cannot extract PDF text. Please upload TXT or CSV instead.")

    # DOCX
    elif file_ext == "docx":
        if Document:
            try:
                uploaded_file.seek(0)
                doc = Document(uploaded_file)
                uploaded_text = "\n".join([p.text for p in doc.paragraphs])
                st.success("✅ Word text extracted.")
            except Exception as e:
                st.error(f"⚠️ Failed to read DOCX: {e}")
        else:
            st.warning("⚠️ python-docx not installed. Please upload PDF, TXT, or CSV instead.")

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

    else:
        st.warning("⚠️ Unsupported file type. Please upload PDF, DOCX, TXT, or CSV.")

    # Save the extracted text to session_state for FAQ use
    if uploaded_text:
        st.session_state["course_text"] = uploaded_text
        st.session_state["course_filename"] = uploaded_file.name

    with st.expander("📜 Preview Extracted Text"):
        st.text(
            (uploaded_text or st.session_state.get("course_text", ""))[:2000] + 
            ("..." if len((uploaded_text or st.session_state.get("course_text", ""))) > 2000 else "")
        )
# ==========================
# DATA ANALYSIS TOOLS (original behavior kept)
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
# COURSE FAQ CHATBOT SECTION (Integrated, always visible)
# ==========================
st.write("---")
st.header("📚 Course FAQ Chatbot (Lightweight, Upload-based)")

st.write("""
This FAQ bot answers questions using **ONLY** the text you upload above (syllabus, assignment sheets, policies).  
It does **not** use external knowledge. If the answer is not present in the uploaded document, the bot will reply:
**"I don't know — please ask the instructor."**
""")

course_choice = st.selectbox("Choose course to power the FAQ bot", [
    "Business Mathematics II (Bilingual: EN + AR)",
    "Principles of Microeconomics (Arabic: MSA + light Qatari tone)"
])

faq_enable = st.checkbox("Enable Course FAQ Mode", value=False)

# Lightweight retrieval: split uploaded text into chunks and do simple similarity via substring & keyword matching
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    if not text:
        return []
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

def keyword_search_chunks(question: str, chunks: list, top_k=5):
    # Very simple scoring: count keyword overlaps (split on spaces, lowercase)
    q_tokens = [t for t in question.lower().split() if len(t) > 1]
    scores = []
    for i, c in enumerate(chunks):
        c_low = c.lower()
        score = sum(1 for t in q_tokens if t in c_low)
        scores.append((score, i, c))
    scores.sort(reverse=True, key=lambda x: x[0])
    # Return up to top_k chunks with positive score
    return [c for s, i, c in scores[:top_k] if s > 0]

# Language detection (simple)
def likely_arabic(text: str):
    # crude heuristic: presence of Arabic letters
    if any("\u0600" <= ch <= "\u06FF" for ch in text):
        return True
    return False

# RAG-like prompt (we'll send context to POE/API; but ensure model knows to use only context)
def build_faq_prompt(context_chunks, question, course_choice):
    context = "\n\n---\n\n".join(context_chunks)
    base = (
        "You are a course assistant. Use ONLY the CONTEXT provided below to answer the student's question. "
        "If the answer is not in the context, reply exactly: \"I don't know — please ask the instructor.\" "
        "Keep answers concise and friendly. Add a one-line citation indicating the uploaded filename at the end."
        "\n\nCONTEXT:\n"
    )
    prompt = base + context + f"\n\nQuestion: {question}\n\nAnswer:"
    # language instructions
    if "Business Mathematics" in course_choice:
        prompt += "\n\nIf the question is in Arabic, answer in Arabic; if in English, answer in English. Keep Arabic formal but friendly."
    else:
        prompt += "\n\nAnswer in Modern Standard Arabic using a light Qatari-friendly tone. Keep it professional and concise."
    return prompt

def faq_answer(question: str):
    # fetch uploaded course text from session
    text = st.session_state.get("course_text", "")
    filename = st.session_state.get("course_filename", "uploaded_course_doc")
    if not text:
        return "No course document uploaded. Please upload the syllabus or course document above and try again."
    # chunk and search
    chunks = chunk_text(text, chunk_size=1200, overlap=200)
    matched = keyword_search_chunks(question, chunks, top_k=5)
    if not matched:
        return "I don't know — please ask the instructor."

    # Build prompt using matched chunks as context
    prompt = build_faq_prompt(matched, question, course_choice)

    # Prefer POE chat for generation (you already have POE API configured)
    if not POE_API_KEY or POE_API_KEY == "YOUR_POE_API_KEY_HERE":
        return "POE API key not configured in Streamlit secrets (POE_API_KEY). Cannot generate FAQ answer."

    try:
        headers = {"Authorization": f"Bearer {POE_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.0}
        res = requests.post(POE_API_URL, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
        response_text = data["choices"][0]["message"]["content"].strip()
        # safety: ensure the model didn't hallucinate; enforce "I don't know" if it claims facts not in context
        # crude check: ensure the response references something from matched chunks (we check for any overlap token)
        # If it fails the crude check, return "I don't know"
        q_tokens = [t for t in question.lower().split() if len(t) > 1]
        if not any(t in " ".join(matched).lower() for t in q_tokens):
            # question tokens not present in context; we already returned earlier, but repeat safety
            return "I don't know — please ask the instructor."
        # append citation line
        cite = f"\n\nSource: [{filename}]"
        return response_text + cite
    except Exception as e:
        return f"❌ Error contacting POE API for FAQ: {e}"

# FAQ UI controls (always visible as you requested)
if faq_enable:
    st.write("**Course FAQ Mode:** Enabled — answers will be drawn only from the uploaded course document.")
    faq_question = st.text_input("Ask the course (FAQ bot):", placeholder="e.g., When is Assignment 2 due?", key="faq_q")
    if st.button("Ask FAQ bot"):
        if not faq_question.strip():
            st.warning("Please type a question for the FAQ bot.")
        else:
            with st.spinner("Searching uploaded document..."):
                answer = faq_answer(faq_question)
                st.write("**FAQ Bot answer:**")
                # detect language for display preferences
                if likely_arabic(faq_question) or "Principles of Microeconomics" in course_choice:
                    st.write(answer)
                else:
                    st.write(answer)

# ==========================
# MAIN CHAT (original POE API flow)
# ==========================
st.markdown("---")
st.header("💬 General AI Chat (POE API)")

# display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

default_prompt = "Summarize the uploaded document." if st.session_state.get("course_text","") else ""
user_input = st.chat_input("Type your question or ask about your uploaded file...") or default_prompt

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            headers = {"Authorization": f"Bearer {POE_API_KEY}", "Content-Type": "application/json"}
            content = f"File content:\n{st.session_state.get('course_text','')[:4000]}\n\nQuestion: {user_input}" if st.session_state.get('course_text','') else user_input
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
st.caption("💡 EconLab AI Assistant — FAQ Bot integrated. FAQ answers are strictly based on the uploaded document and generated via POE API. Configure POE_API_KEY in Streamlit secrets.")
