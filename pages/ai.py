import streamlit as st
import zhipuai

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input (Zhipu AI key)
api_key = st.text_input("Enter your Zhipu AI API Key:", type="password")

# Prompt input
prompt = st.text_area("💬 Ask a question about economics:", height=150)

# Optional settings
with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    top_p = st.slider("Top-p (nucleus sampling)", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 256, 4096, 1024, 128)

# Generate Answer
if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your Zhipu AI API key.")
    elif not prompt.strip():
        st.error("❌ Please write a prompt.")
    else:
        try:
            zhipuai.api_key = api_key
            response = zhipuai.model_api.sse_invoke(
                model="glm-4.5",
                prompt=[
                    {"role": "system", "content": "You are an expert in economics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=False
            )
            answer = response["data"]
            st.markdown("### 🤖 Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
