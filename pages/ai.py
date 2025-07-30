import streamlit as st
import zhipuai

st.set_page_config(page_title="🧠 AI Economics Assistant (GLM)", layout="centered")
st.title("🧠 AI Economics Assistant (GLM-4.5)")

# API Key input (Zhipu AI key)
api_key = st.text_input("00d0e718244f4eb4a1c0c1fc85640a11.THXr41nPePMMx9z4:", type="password")
# Input user prompt
prompt = st.text_area("💬 Ask your economics question:")

# Optional model settings
with st.expander("⚙️ Advanced Settings"):
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.05)
    top_p = st.slider("Top-p", 0.1, 1.0, 0.95, 0.05)
    model = st.selectbox("Model", ["glm-4", "glm-4.5"], index=1)

# Generate answer on button click
if st.button("🚀 Get Answer"):
    if not api_key:
        st.error("❌ Please provide your ZhipuAI API key.")
    elif not prompt.strip():
        st.error("❌ Please enter a question.")
    else:
        try:
            # Set the API key
            zhipuai.api_key = api_key

            # Create chat completion
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": "Hello, ZhipuAI!"}
    ]
)
print(response.choices[0].message.content)

            # Send the chat request
            response = client.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an economics assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=top_p,
            )

            # Display result
            answer = response['data']['choices'][0]['content']
            st.markdown("### 🤖 Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ Error: {e}")
