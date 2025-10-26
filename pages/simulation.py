import streamlit as st
import requests
import json
import time
import pandas as pd
import io

# Optional imports for PDF/DOCX parsing
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
# POE API CONFIG
# ==========================
POE_API_URL = "https://api.poe.com/v1/chat/completions"
POE_API_KEY = st.secrets.get("POE_API_KEY", "YOUR_POE_API_KEY_HERE")
MODEL = st.selectbox("Select model", ["maztouriabot", "gpt-4o-mini", "claude-3-haiku"])

# ==========================
# STATE INIT
# ==========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "course_text" not in st.session_state:
    st.session_state["course_text"] = ""
if "course_filename" not in st.session_state:
    st.session_state["course_filename"] = ""

# ==========================
# FILE UPLOAD
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
        uploaded_file_obj.seek(0)
        return pd.read_csv(uploaded_file_obj, encoding="latin1")

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    if file_ext == "pdf" and PdfReader:
        uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
        uploaded_text = "\n\n".join([p.extract_text() or "" for p in reader.pages])
    elif file_ext == "docx" and Document:
        uploaded_file.seek(0)
        doc = Document(uploaded_file)
        uploaded_text = "\n".join([p.text for p in doc.paragraphs])
    elif file_ext == "txt":
        uploaded_file.seek(0)
        uploaded_text = uploaded_file.read().decode("utf-8", errors="ignore")
    elif file_ext == "csv":
        uploaded_file.seek(0)
        df = safe_read_csv(uploaded_file)
        st.dataframe(df.head())
        uploaded_text = df.to_string(index=False)
    st.session_state["course_text"] = uploaded_text
    st.session_state["course_filename"] = uploaded_file.name
    with st.expander("📜 Preview Extracted Text"):
        st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

# ==========================
# DATA ANALYSIS TOOLS
# ==========================
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except:
    sns = None
try:
    import statsmodels.api as sm
except:
    sm = None

if df is not None:
    st.markdown("### 📊 Data Analysis Tools")
    if st.button("Plot Pairplot"):
        if sns:
            st.pyplot(sns.pairplot(df.select_dtypes(include="number")))
    if sm and st.button("Run OLS Regression"):
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) >= 2:
            y_col = st.selectbox("Dependent variable", numeric_cols, key="ycol")
            X_cols = st.multiselect("Independent variables", [c for c in numeric_cols if c != y_col], key="xcols")
            if X_cols:
                X = sm.add_constant(df[X_cols])
                y = df[y_col]
                model = sm.OLS(y, X).fit()
                st.write(model.summary())

# ==========================
# TRANSLATION HELPER
# ==========================
def translate_to_arabic(text: str):
    if not POE_API_KEY or POE_API_KEY=="YOUR_POE_API_KEY_HERE":
        return "POE API key not configured."
    prompt = f"Translate the following text to Arabic (MSA):\n{text}"
    try:
        res = requests.post(
            POE_API_URL, 
            headers={"Authorization": f"Bearer {POE_API_KEY}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages":[{"role":"user","content":prompt}], "temperature":0.0},
            timeout=60
        )
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Translation error: {e}"

translate_checkbox = st.checkbox("Translate AI responses to Arabic", value=False)

# ==========================
# FAQ BOT
# ==========================
st.write("---")
st.header("📚 Course FAQ Bot")
course_choice = st.selectbox("Choose course", [
    "Business Mathematics II (Bilingual: EN + AR)",
    "Principles of Microeconomics (Arabic)"
])
faq_enable = st.checkbox("Enable Course FAQ Mode", value=False)

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = min(start+chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def keyword_search_chunks(question, chunks, top_k=5):
    q_tokens = [t for t in question.lower().split() if len(t)>1]
    scored = [(sum(1 for t in q_tokens if t in c.lower()), c) for c in chunks]
    return [c for s,c in sorted(scored, reverse=True)[:top_k] if s>0]

def faq_answer(question):
    text = st.session_state.get("course_text","")
    if not text: return "No course document uploaded."
    chunks = chunk_text(text)
    matched = keyword_search_chunks(question, chunks)
    if not matched: return "I don't know — please ask the instructor."
    prompt = f"Answer the question using ONLY the following context:\n\n{'---'.join(matched)}\n\nQuestion: {question}\nAnswer:"
    try:
        res = requests.post(
            POE_API_URL,
            headers={"Authorization":f"Bearer {POE_API_KEY}","Content-Type":"application/json"},
            json={"model":MODEL,"messages":[{"role":"user","content":prompt}], "temperature":0.0},
            timeout=60
        )
        res.raise_for_status()
        answer = res.json()["choices"][0]["message"]["content"].strip()
        if translate_checkbox:
            answer = translate_to_arabic(answer)
        return answer + f"\n\nSource: [{st.session_state.get('course_filename','uploaded_doc')}]"
    except Exception as e:
        return f"❌ POE API error: {e}"

if faq_enable:
    faq_q = st.text_input("Ask the course FAQ bot:")
    if st.button("Ask FAQ bot"):
        if faq_q.strip():
            st.write(faq_answer(faq_q))
        else:
            st.warning("Type a question first.")

# ==========================
# MAIN CHAT
# ==========================
st.markdown("---")
st.header("💬 General AI Chat")
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

default_prompt = "Summarize the uploaded document." if st.session_state.get("course_text","") else ""
user_input = st.chat_input("Type your question...") or default_prompt

if user_input:
    st.session_state["messages"].append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            content = f"File content:\n{st.session_state.get('course_text','')[:4000]}\n\nQuestion: {user_input}" if st.session_state.get('course_text') else user_input
            res = requests.post(
                POE_API_URL,
                headers={"Authorization":f"Bearer {POE_API_KEY}","Content-Type":"application/json"},
                json={"model":MODEL,"messages":[{"role":"user","content":content}]},
                timeout=60
            )
            res.raise_for_status()
            response_text = res.json()["choices"][0]["message"]["content"]
            for token in response_text.split():
                full_response += token + " "
                placeholder.markdown(full_response + "▌")
                time.sleep(0.03)
            if translate_checkbox:
                full_response = translate_to_arabic(full_response)
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"❌ Error fetching response: {e}")
            full_response = f"Error: {e}"
    st.session_state["messages"].append({"role":"assistant","content":full_response})

# ==========================
# EXPORT CHAT
# ==========================
st.markdown("---")
col1,col2,col3 = st.columns([1,1,2])
if col1.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared!")
if col2.button("💾 Export Chat"):
    if st.session_state["messages"]:
        st.download_button("Download CSV", pd.DataFrame(st.session_state["messages"]).to_csv(index=False), "econlab_chat.csv", "text/csv")
    else:
        st.warning("No chat to export!")

st.caption("💡 EconLab AI Assistant — FAQ + Translation integrated. Configure POE_API_KEY in Streamlit secrets.")
