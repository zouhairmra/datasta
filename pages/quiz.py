import streamlit as st
import random
import pandas as pd
# RTL support
st.markdown("<style>body {direction: RTL; text-align: right;}</style>", unsafe_allow_html=True)

st.title("🧠 اختبار في الاقتصاد والإحصاء")

# --- Sample Questions
questions = [
    {
        "question": "ما هو الناتج المحلي الإجمالي؟",
        "options": ["إجمالي الصادرات", "قيمة السلع والخدمات المنتجة محليًا", "الضرائب الحكومية", "الاحتياطي النقدي"],
        "answer": "قيمة السلع والخدمات المنتجة محليًا"
    },
    {
        "question": "ما هو الانحدار الخطي؟",
        "options": ["اختبار توزيع", "علاقة بين متغيرين", "مقياس تباين", "مقياس وسط حسابي"],
        "answer": "علاقة بين متغيرين"
    },
    {
        "question": "أي من التالي يعتبر مؤشرًا للتضخم؟",
        "options": ["مؤشر أسعار المستهلك", "معدل البطالة", "العرض النقدي", "سعر الفائدة"],
        "answer": "مؤشر أسعار المستهلك"
    },
]

# Shuffle questions once per session
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = random.sample(questions, len(questions))
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []

# Display current question
q = st.session_state.quiz_data[st.session_state.current_q]
st.subheader(f"❓ السؤال {st.session_state.current_q + 1} من {len(questions)}")
selected = st.radio(q["question"], q["options"], key=f"q{st.session_state.current_q}")

if st.button("✅ إرسال"):
    is_correct = selected == q["answer"]
    st.session_state.answers.append({
        "question": q["question"],
        "selected": selected,
        "correct": q["answer"],
        "is_correct": is_correct
    })

    if is_correct:
        st.success("✅ إجابة صحيحة!")
        st.session_state.score += 1
    else:
        st.error(f"❌ خطأ. الإجابة الصحيحة: {q['answer']}")

    # Move to next question
    if st.session_state.current_q + 1 < len(questions):
        st.session_state.current_q += 1
        st.rerun()
    else:
        st.balloons()
        st.markdown("### 🏁 انتهى الاختبار")
        st.write(f"🎯 النتيجة: {st.session_state.score} من {len(questions)}")

        # Show detailed results
        df_results = pd.DataFrame(st.session_state.answers)
        st.dataframe(df_results)

        # --- Export
        if st.download_button("📥 تحميل النتائج بصيغة CSV", df_results.to_csv(index=False), "quiz_results.csv", "text/csv"):
            st.success("✅ تم التحميل!")

        # Reset button
        if st.button("🔁 أعد الاختبار"):
            for key in ["quiz_data", "current_q", "score", "answers"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()
