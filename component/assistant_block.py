# components/assistant_block.py

import streamlit as st
import requests

def run_assistant_block(payload, url, headers, selected_model):
    st.markdown("## 🤖 AI Assistant")

    with st.expander("📦 Show Request Payload"):
        st.json(payload)

    if st.button("🔁 Re-run"):
        try:
            resp = requests.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                st.session_state.answer = answer  # save for later use
                st.markdown("### 🤖 Answer")
                st.write(answer)
            else:
                st.error(f"❌ HTTP {resp.status_code}: {resp.json()}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

    # 📝 Answer summarization
    with st.expander("📝 Summarize Answer"):
        if "answer" in st.session_state and st.button("🔍 Summarize the previous answer"):
            summary_payload = {
                "model": selected_model,
                "messages": [
                    {"role": "system", "content": "Summarize the following answer clearly and concisely."},
                    {"role": "user", "content": st.session_state.answer}
                ],
                "temperature": 0.3,
                "max_tokens": 200
            }
            try:
                sum_resp = requests.post(url, headers=headers, json=summary_payload)
                if sum_resp.status_code == 200:
                    summary = sum_resp.json()["choices"][0]["message"]["content"]
                    st.markdown("### ✂️ Summary")
                    st.write(summary)
                else:
                    st.error("❌ Failed to summarize.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
