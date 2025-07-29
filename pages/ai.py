import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="🧠 AI Economics Assistant", layout="centered")
st.title("🧠 AI Economics Assistant (ChatGPT)")

# OpenAI API Key input
api_key = st.text_input("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", type="password")

# Prompt input
prompt = st.text_area("💬 Ask a question about economics:", height=150)

# Optional settings
with st.expander("🧠 Model Options"):
    model = st.selectbox(
        "Choose a model",
        ["gpt-3.5-turbo", "gpt-4"],
        index=0
    )

with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 256, 4096, 1024, 128)

# Generate Answer
if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your OpenAI API key.")
    elif not prompt.strip():
        st.error("❌ Please write a prompt.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert in economics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            answer = response.choices[0].message.content
            st.markdown("### 🤖 Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
