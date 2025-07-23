import streamlit as st

def select_language():
    return st.sidebar.selectbox("🌐 Language", ["English", "العربية"])
    from components.language_selector import select_language

lang = select_language()

if lang == "English":
    st.title("Upload Your Data")
else:
    st.title("تحميل البيانات الخاصة بك")
