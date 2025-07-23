import streamlit as st
import requests
from transformers import pipeline

# --- Optional: Hugging Face translation model
@st.cache_resource
def get_translation_pipeline():
    return pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")

# --- Assistant block main function
def run_assistant_block():
    st.header("🧠 AI Assistant")

    # --- Model & API Setup
    api_key = st.secrets.get("openai_api_key", "") or st.text_input("🔐 Enter your OpenAI API Key:", type="password")
    if not api_key:
        st.warning("Please enter your API key to continue.")
        return

    model_options = ["gpt-3.5-turbo", "gpt-4"]
    selected_model = st.selectbox("Select Model", model_options)

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # --- User Input
    user_input = st.text_area("💬 Ask something (English or Arabic):")

    # --- Send request
    if st.button("🚀 Get Answer") and user_input:
        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7,
            "max_tokens": 600
        }

        try:
            resp = requests.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                st.markdown("### 🤖 Answer")
                st.write(answer)

                # Option to translate
                if st.toggle("🌐 Translate to Arabic"):
                    translator = get_translation_pipeline()
                    translation = translator(answer, max_length=1000)[0]["translation_text"]
                    st.markdown("### 🌍 الترجمة إلى العربية")
                    st.write(translation)

                # Save to session for summary
                st.session_state["last_answer"] = answer

            else:
                st.error(f"❌ HTTP {resp.status_code}: {resp.json()}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    # --- Show JSON payload
    with st.expander("📦 Show Request Payload"):
        st.json(payload if "payload" in locals() else {})

    # --- Rerun
    if st.button("🔁 Re-run"):
        st.experimental_rerun()

    # --- Upload file for RAG-style context
    with st.expander("📄 Upload File for Context"):
        uploaded_file = st.file_uploader("Upload a text/PDF file", type=["txt", "pdf"])
        if uploaded_file:
            import PyPDF2
            if uploaded_file.name.endswith(".pdf"):
                reader = PyPDF2.PdfReader(uploaded_file)
                file_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            else:
                file_text = uploaded_file.read().decode("utf-8")

            st.success("✅ File uploaded and processed.")
            st.text_area("📜 Extracted Content", file_text[:1000] + "..." if len(file_text) > 1000 else file_text)

            # Append context
            payload["messages"].insert(0, {
                "role": "system",
                "content": f"Use the following document as context:\n{file_text[:3000]}"
            })

    # --- Summarize Answer
    with st.expander("📝 Summarize Answer"):
        if st.button("🔍 Summarize the previous answer"):
            last_answer = st.session_state.get("last_answer")
            if not last_answer:
                st.warning("No answer to summarize.")
                return

            summary_payload = {
                "model": selected_model,
                "messages": [
                    {"role": "system", "content": "Summarize the following answer clearly and concisely."},
                    {"role": "user", "content": last_answer}
                ],
                "temperature": 0.3,
                "max_tokens": 200
            }

            try:
                sum_resp = requests.post(url, headers=headers, json=summary_payload)
                if sum_resp.status_code == 200:
                    summary = sum_resp.json()["choices"][0]["message"]["content"]
                    st.markdown("### ✂️ Summary")
                    st.write(summary)
                else:
                    st.error("❌ Failed to summarize.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
