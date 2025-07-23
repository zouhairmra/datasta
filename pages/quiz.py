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
questions_easy = [
    ("ما هو الناتج المحلي الإجمالي؟", "إجمالي القيمة المضافة في الاقتصاد"),
    ("GDP stands for?", "Gross Domestic Product"),
    ("ما هو قانون الطلب؟", "علاقة عكسية بين السعر والكمية المطلوبة"),
    ("What does CPI measure?", "Consumer Price Index")
]

questions_medium = [
    ("ما هو الانحدار الخطي البسيط؟", "نموذج يربط متغير تابع بمتغير مستقل"),
    ("What is p-value used for?", "To test statistical significance"),
    ("ما هي مرونة الطلب السعرية؟", "قياس استجابة الطلب لتغير السعر"),
    ("OLS stands for?", "Ordinary Least Squares")
]

questions_hard = [
    ("في اختبار F، ما هي الفرضية الصفرية؟", "جميع المعاملات تساوي صفر"),
    ("What does heteroskedasticity imply?", "Non-constant variance of errors"),
    ("ما الفرق بين التباين والانحراف المعياري؟", "التباين هو مربع الانحراف المعياري"),
    ("What does R-squared measure?", "Proportion of variance explained")
]

questions_pool = {
    "Easy": questions_easy,
    "Medium": questions_medium,
    "Hard": questions_hard
}

# Use a default username if none set (for example, guest user)
if 'username' not in locals() and 'username' not in globals():
    username = "guest_user"

question, correct_answer = random.choice(questions_pool[difficulty])
user_answer = st.text_input(t("السؤال:", "Question:") + f" {question}")

if st.button(t("إرسال", "Submit")):
    if user_answer.strip().lower() == correct_answer.lower():
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
