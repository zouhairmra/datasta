import streamlit as st
import numpy as np
import pandas as pd
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Economic Simulation Center", layout="wide")

# Securely load your OpenAI API key
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Translation helper
language = st.radio("🌐 Choose Language / اختر اللغة", ["English", "العربية"])

def translate(en, ar):
    return ar if language == "العربية" else en

st.title(translate("📊 Economic Simulation Center", "📊 مركز محاكاة الاقتصاد"))

# Sidebar navigation
section = st.sidebar.selectbox(
    translate("Choose Section", "اختر القسم"),
    [
        translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"),
        translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"),
        translate("AI Assistant", "المساعد الذكي")
    ]
)

# --- Microeconomics simulations ---
if section == translate("Microeconomics Simulations", "محاكاة الاقتصاد الجزئي"):
    # (Keep all your simulation code here unchanged)
    # This part is okay and already working
    pass

# --- Business Math Concepts ---
elif section == translate("Business Math Concepts", "مفاهيم الرياضيات للأعمال"):
    # (Keep your business math simulation code here unchanged)
    pass

# --- AI Assistant Section ---
elif section == translate("AI Assistant", "المساعد الذكي"):

    st.header(translate("Ask the AI Assistant", "اسأل المساعد الذكي"))

    user_question = st.text_area(translate(
        "Ask any question related to microeconomics or business math.",
        "اطرح أي سؤال متعلق بالاقتصاد الجزئي أو الرياضيات للأعمال."
    ))

    if user_question:
        with st.spinner(translate("Thinking...", "جارٍ التفكير...")):
            try:
                chat_completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert assistant helping Arabic-speaking students understand microeconomics and business mathematics. Use simple examples and explain clearly."},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                answer = chat_completion.choices[0].message.content
                st.success(answer)

            except Exception as e:
                st.error(f"Error communicating with OpenAI API: {e}")
