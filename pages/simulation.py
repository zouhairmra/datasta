import streamlit as st
import requests
import json
import time
import pandas as pd

# ==========================
# OPTIONAL LIBRARIES
# ==========================
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
    st.warning("⚠️ PyPDF2 not found. PDF upload disabled.")

try:
    from docx import Document
except ImportError:
    Document = None
    st.warning("⚠️ python-docx not found. Word file upload disabled.")

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    st.warning("⚠️ matplotlib not found. Plotting disabled.")

try:
    import seaborn as sns
except ImportError:
    sns = None
    st.warning("⚠️ seaborn not found. Advanced plotting disabled.")

try:
    import statsmodels.api as sm
except ImportError:
    sm = None
    st.warning("⚠️ statsmodels not found. Regression analysis unavailable.")

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
# FILE UPLOAD
# ==========================
st.markdown("### 📂 Upload a file for AI analysis")
uploaded_file = st.file_uploader("Upload PDF, CSV, or Word", type=["pdf", "csv", "docx"])
uploaded_text = ""
df = None

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    # PDF
    if file_ext == "pdf" and PdfReader:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            uploaded_text += page.extract_text() or ""
        st.success("✅ PDF text extracted.")
    
    # Word
    elif file_ext == "docx" and Document:
        doc = Document(uploaded_file)
        uploaded_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("✅ Word text extracted.")
    
    # CSV
    elif file_ext == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        uploaded_text = df.to_string(index=False)
        st.success("✅ CSV data loaded.")

    with st.expander("📜 Preview Extracted Text"):
        st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

# ==========================
# DATA ANALYSIS BUTTONS
# ==========================
if df is not None:
    st.markdown("### 📊 Data Analysis Tools")

    if plt and st.button("Plot Pairplot (Seaborn)"):
        if sns:
            st.write("Generating pairplot...")
            fig = sns.pairplot(df.select_dtypes(include="number"))
            st.pyplot(fig)
        else:
            st.warning("⚠️ seaborn not installed. Cannot generate pairplot.")

    if sm and st.button("Run OLS Regression (Statsmodels)"):
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) >= 2:
            y_col = st.selectbox("Select dependent variable", numeric_cols)
            X_cols = st.multiselect("Select independent variables", [c for c in numeric_cols if c != y_col])
            if X_cols:
                X = sm.add_constant(df[X_cols])
                y = df[y_col]
                model = sm.OLS(y, X).fit()
                st.write(model.summary())
        else:
            st.warning("Not enough numeric columns for regression.")

# ==========================
# CHAT MEMORY
# ==========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================
# USER INPUT
# ==========================
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
st.caption("💡 EconLab AI Assistant — Powered by Poe API and Streamlit.")
