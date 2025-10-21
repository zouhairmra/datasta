import streamlit as st
from zhipuai import ZhipuAI

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM-4.5)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input
api_key = st.text_input("🔑 Enter your ZhipuAI API Key:", type="password")
# Initialize or load chat history (system + past user + assistant messages)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an expert in economics."}
    ]

# Display chat history
for msg in st.session_state.chat_history[1:]:  # skip system message from display
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Assistant:** {msg['content']}")

# Prompt input
user_input = st.text_area("💬 Your question:", height=150)

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
    elif not user_input.strip():
        st.error("❌ Please write a prompt.")
    else:
        try:
            client = ZhipuAI(api_key=api_key)

            # Add user input to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

            # Send entire chat history for context
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.chat_history,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            # Stream response and build assistant's message
            answer_container = st.empty()
            answer_text = ""
            for chunk in response:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    answer_text += delta.content
                    answer_container.markdown(answer_text)

            # Append assistant's answer to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": answer_text})

        except Exception as e:
            st.error(f"❌ Error: {e}")
