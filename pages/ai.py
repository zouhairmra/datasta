import streamlit as st
from gpt4all import GPT4All

# -------------------------------------------------
# 1️⃣ PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="🧠 Local AI Economics Assistant", layout="centered")
st.title("🧠 Local AI Economics Assistant")

# -------------------------------------------------
# 2️⃣ MODEL CONFIGURATION
# -------------------------------------------------
with st.expander("🧠 Model Options"):
    model_path = st.text_input(
        "Enter the path to your local model (.gguf):",
        value="models/phi-3-mini-4k-instruct.Q4_0.gguf"
    )
    model_name = model_path.split("/")[-1]
    st.write(f"🔍 Using model: **{model_name}**")

with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 64, 1024, 512, 64)

# -------------------------------------------------
# 3️⃣ CHAT HISTORY
# -------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an expert in economics."}
    ]

for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Assistant:** {msg['content']}")

# -------------------------------------------------
# 4️⃣ USER INPUT
# -------------------------------------------------
user_input = st.text_area("💬 Your question:", height=150)

# -------------------------------------------------
# 5️⃣ GENERATE ANSWER
# -------------------------------------------------
if st.button("Generate Answer"):
    if not user_input.strip():
        st.error("❌ Please enter a question.")
    else:
        try:
            # Load local model
            model = GPT4All(model_name=model_path)

            # Add user input
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

            # Build the conversation as prompt
            prompt = "\n".join(
                [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history]
            ) + "\nAssistant:"

            # Generate local model response
            with model.chat_session():
                response = model.generate(
                    prompt,
                    temp=temperature,
                    max_tokens=max_tokens
                )

            # Show and store answer
            st.markdown(f"🤖 **Assistant:** {response}")
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ Error: {e}")
