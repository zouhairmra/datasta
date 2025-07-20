import streamlit as st
from llama_cpp import Llama


@st.cache_resource
def load_model():
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,  # adjust depending on your CPU
        n_gpu_layers=0  # set >0 if you want to use GPU acceleration
    )

llm = load_model()

st.title("🧠 Local AI Chatbot (Phi-3)")
st.write("Ask any question below (runs offline, no API key required).")

user_input = st.text_input("You:", key="input")

if user_input:
    with st.spinner("Thinking..."):
        response = llm(
            f"<|system|>You are a helpful assistant.<|user|>{user_input}<|assistant|>",
            max_tokens=512,
            stop=["<|user|>", "<|assistant|>"]
        )
        output = response["choices"][0]["text"]
        st.markdown(f"**Bot:** {output.strip()}")
