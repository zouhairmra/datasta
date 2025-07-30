import streamlit as st
import zhipuai

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input (Zhipu AI key)
api_key = st.text_input("00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4:", type="password")
# Prompt input
prompt = st.text_area("💬 Ask a question about economics:", height=150)

# Model options (optional)
with st.expander("🧠 Model Options"):
    model = st.selectbox("Choose a model", ["glm-4.5", "glm-4", "chatglm3-6b"], index=0)

# Advanced settings
with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max Tokens", 128, 4096, 1024, 128)

# Generate Answer
if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your Zhipu.AI API key.")
    elif not prompt.strip():
        st.error("❌ Please enter a prompt.")
    else:
        try:
            zhipuai.api_key = api_key
            response = zhipuai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert in economics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
            answer = response['choices'][0]['message']['content']
            st.markdown("### 🤖 Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
