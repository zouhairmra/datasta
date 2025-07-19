# pages/chatbot.py
import streamlit as st

st.set_page_config(page_title="Simple Chatbot", page_icon="💬")
st.title("🤖 Simple Rule-Based Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def rule_based_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! 👋"
    elif "how are you" in user_input:
        return "I'm doing great, thanks!"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day 😊"
    else:
        return "I'm just a simple bot. Ask me something like 'hello', 'how are you', or 'bye'."

# Chat UI
user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    response = rule_based_response(user_input)
    st.session_state.chat_history.append(("bot", response))

# Show chat history
for speaker, message in st.session_state.chat_history:
    with st.chat_message("user" if speaker == "user" else "assistant"):
        st.markdown(message)
