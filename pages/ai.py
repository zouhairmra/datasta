import streamlit as st
import zhipuai

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input (Zhipu AI key)
api_key = st.text_input("00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4:", type="password")
# Prompt input
prompt = st.text_area("💬 Ask your economics question:", height=150)

# Optional settings
with st.expander("⚙️ Model Settings"):
    model = st.selectbox("Choose model", ["glm-4", "glm-4.5"], index=1)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.05)
    top_p = st.slider("Top-p (nucleus sampling)", 0.1, 1.0, 0.9, 0.05)

# Submit button
if st.button("🚀 Get Answer"):
    if not api_key:
        st.error("❌ Please enter your ZhipuAI API key.")
    elif not prompt.strip():
        st.error("❌ Please enter a prompt.")
    else:
        try:
            # Set API key
            zhipuai.api_key = api_key

            # Send request
            response = zhipuai.model_api.sse_invoke(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an economics assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                incremental=False  # set to True if you want streaming tokens
            )

            # Display result
            answer = response['data']['choices'][0]['content']
            st.markdown("### 🤖 Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ Error: {e}")
