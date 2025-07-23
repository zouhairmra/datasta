import streamlit as st
import random
from db import save_score, load_scores
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --------------------
# RTL layout for Arabic
# --------------------
st.markdown("""
    <style>
        body {direction: RTL; text-align: right;}
        .block-container {padding: 1rem;}
    </style>
""", unsafe_allow_html=True)

# --------------------
# Load Authenticator Config
# --------------------
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"], config["cookie"]["name"],
    config["cookie"]["key"], config["cookie"]["expiry_days"]
)

name, auth_status, username = authenticator.login("Login", location="main")

if auth_status is False:
    st.error("اسم المستخدم أو كلمة السر غير صحيحة")
    st.stop()
elif auth_status is None:
    st.warning("الرجاء إدخال اسم المستخدم وكلمة السر")
    st.stop()

# --------------------
# Language Toggle
# --------------------
lang = st.radio("اللغة | Language", ["Arabic", "English"], horizontal=True)

def t(ar, en):
    return ar if lang == "Arabic" else en

st.title(t("📘 صفحة الاختبارات", "📘 Quiz Page"))

# --------------------
# Difficulty Selection
# --------------------
difficulty = st.selectbox(
    t("اختر مستوى الصعوبة", "Select Difficulty"),
    ["Easy", "Medium", "Hard"]
)

# --------------------
# Randomized Questions
# --------------------
questions_easy = [("2+2", "4"), ("5-3", "2")]
questions_medium = [("10/2", "5"), ("3*4", "12")]
questions_hard = [("sqrt(16)", "4"), ("log(100,10)", "2")]

questions_pool = {
    "Easy": questions_easy,
    "Medium": questions_medium,
    "Hard": questions_hard
}

question, correct_answer = random.choice(questions_pool[difficulty])
user_answer = st.text_input(t("السؤال:", "Question:") + f" {question}")

if st.button(t("إرسال", "Submit")):
    if user_answer.strip() == correct_answer:
        st.success(t("إجابة صحيحة ✅", "Correct ✅"))
        save_score(username, 1, difficulty)
    else:
        st.error(t(f"إجابة خاطئة ❌، الصحيح هو: {correct_answer}", f"Incorrect ❌. Correct answer: {correct_answer}"))
        save_score(username, 0, difficulty)

# --------------------
# Show Previous Scores
# --------------------
if st.checkbox(t("📊 عرض النتائج السابقة", "📊 Show Previous Scores")):
    scores = load_scores(username)
    st.dataframe(scores)

# --------------------
# Export to CSV
# --------------------
if st.button(t("📥 تحميل النتائج كـ CSV", "📥 Export Results as CSV")):
    scores = load_scores(username)
    st.download_button(
        label=t("تحميل", "Download"),
        data=scores.to_csv(index=False).encode('utf-8-sig'),
        file_name="scores.csv",
        mime="text/csv"
    )
