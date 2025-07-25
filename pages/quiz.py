import streamlit as st
import random
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

import random

# --------------------
# Multiple Choice Questions
# --------------------
questions_easy = [
    {
        "question_en": "What does GDP stand for?",
        "question_ar": "ما هو الناتج المحلي الإجمالي؟",
        "options_en": ["Gross Domestic Product", "General Domestic Product", "Great Domestic Product", "Global Domestic Product"],
        "options_ar": ["إجمالي الناتج المحلي", "الناتج المحلي العام", "الناتج المحلي العظيم", "الناتج المحلي العالمي"],
        "answer": "Gross Domestic Product"
    },
    {
        "question_en": "What does CPI measure?",
        "question_ar": "ما الذي يقيسه مؤشر أسعار المستهلك؟",
        "options_en": ["Consumer Price Index", "Cost Price Index", "Consumer Product Indicator", "Cost Product Indicator"],
        "options_ar": ["مؤشر أسعار المستهلك", "مؤشر سعر التكلفة", "مؤشر منتج المستهلك", "مؤشر تكلفة المنتج"],
        "answer": "Consumer Price Index"
    }
]

questions_medium = [
    {
        "question_en": "What is p-value used for?",
        "question_ar": "ما هو استخدام قيمة p؟",
        "options_en": ["Testing significance", "Measuring mean", "Calculating variance", "Estimating slope"],
        "options_ar": ["اختبار الدلالة", "قياس المتوسط", "حساب التباين", "تقدير الميل"],
        "answer": "Testing significance"
    },
    {
        "question_en": "What does OLS stand for?",
        "question_ar": "ما معنى OLS؟",
        "options_en": ["Ordinary Least Squares", "Optimal Least Squares", "Ordered Linear System", "Overall Least Squares"],
        "options_ar": ["المربعات الصغرى العادية", "المربعات الصغرى المثلى", "النظام الخطي المرتب", "المربعات الصغرى الشاملة"],
        "answer": "Ordinary Least Squares"
    }
]

questions_hard = [
    {
        "question_en": "What does heteroskedasticity imply?",
        "question_ar": "ماذا يعني التغاير غير المتجانس؟",
        "options_en": [
            "Non-constant variance of errors",
            "Constant variance of errors",
            "Errors are independent",
            "Errors have zero mean"
        ],
        "options_ar": [
            "تباين غير ثابت للأخطاء",
            "تباين ثابت للأخطاء",
            "الأخطاء مستقلة",
            "متوسط الأخطاء صفر"
        ],
        "answer": "Non-constant variance of errors"
    },
    {
        "question_en": "What does R-squared measure?",
        "question_ar": "ما الذي يقيسه R-مربع؟",
        "options_en": [
            "Proportion of variance explained",
            "Average value of residuals",
            "Slope of regression line",
            "Correlation between variables"
        ],
        "options_ar": [
            "نسبة التباين المفسرة",
            "متوسط القيم المتبقية",
            "ميل خط الانحدار",
            "الارتباط بين المتغيرات"
        ],
        "answer": "Proportion of variance explained"
    }
]

questions_pool = {
    "Easy": questions_easy,
    "Medium": questions_medium,
    "Hard": questions_hard
}

# Ensure username default
if 'username' not in locals() and 'username' not in globals():
    username = "guest_user"

# Select question based on difficulty
q = random.choice(questions_pool[difficulty])

# Extract question and options based on selected language
question_text = q["question_ar"] if lang == "Arabic" else q["question_en"]
options = q["options_ar"] if lang == "Arabic" else q["options_en"]
correct_answer = q["answer"]

# Shuffle options for randomness
random.shuffle(options)

st.write(f"**{t('السؤال:', 'Question:')}** {question_text}")

# Radio button for multiple choice
user_answer = st.radio(t("اختر إجابتك:", "Choose your answer:"), options)

if st.button(t("إرسال", "Submit")):
    if user_answer == correct_answer:
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
