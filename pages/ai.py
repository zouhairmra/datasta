import streamlit as st
from zhipuai import ZhipuAI

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM-4.5)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input
api_key = st.text_input("00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4:", type="password")

# Prompt input
prompt = st.text_area("💬 Ask a question about economics:", height=150)

# Optional settings
with st.expander("🧠 Model Options"):
    model = st.selectbox(
        "Choose a model",
        ["glm-4", "glm-4f", "glm-4b"],  # example GLM models
        index=0
    )

with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 256, 4096, 1024, 128)

if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your ZhipuAI API key.")
    elif not prompt.strip():
        st.error("❌ Please write a prompt.")
    else:
        try:
            client = ZhipuAI(api_key=api_key)
            
            messages = [
                {"role": "system", "content": "You are an expert in economics."},
                {"role": "user", "content": prompt}
            ]
            
            # Streaming response
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            
            # Show streaming output in the app
            answer_container = st.empty()
            answer_text = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    answer_text += delta.content
                    answer_container.markdown(answer_text)
                    
        except Exception as e:
            st.error(f"❌ Error: {e}")
