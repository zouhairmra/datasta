import streamlit as st
from llama_cpp import Llama

# -------------------------------------------------
# 1️⃣ PAGE SETUP
# -------------------------------------------------
st.set_page_config(page_title="🧠 Local LLaMA Economics Assistant", layout="centered")
st.title("🦙 Local LLaMA Economics Assistant")

# -------------------------------------------------
# 2️⃣ MODEL CONFIGURATION
# -------------------------------------------------
with st.expander("🧠 Model Options"):
    model_path = st.text_input(
        "Enter path to your LLaMA model (.gguf):",
        value="models/phi-3-mini-4k-instruct.Q4_0.gguf"  # change to your model path
    )
    st.write(f"🔍 Using model: **{model_path.split('/')[-1]}**")

with st.expander("🔧 Advanced Settings"):
    temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens (response length)", 64, 2048, 512, 64)

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
            # Load LLaMA model
            st.write("⏳ Loading local model... (first time may take a few seconds)")
            llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=4,  # adjust based on your CPU
                verbose=False
            )

            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

            # Build conversation prompt
            messages = "\n".join(
                [f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_history]
            ) + "\nAssistant:"

            # Generate response
            st.write("🤖 Generating response...")
            output = llm(
                messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=["User:", "Assistant:"]
            )

            response = output["choices"][0]["text"].strip()

            # Display and store
            st.markdown(f"🤖 **Assistant:** {response}")
            st.session_state.chat_history.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ Error: {e}")
