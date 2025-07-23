import streamlit as st
import streamlit as st
import statsmodels.api as sm
import pandas as pd
# In sidebar or top of app
language = st.selectbox("🌐 Choose Language", ["English", "Arabic"])
st.session_state.lang = language
labels = {
    "Upload File": {"English": "Upload File", "Arabic": "تحميل الملف"},
    "AI Answer": {"English": "AI Answer", "Arabic": "إجابة الذكاء الاصطناعي"},
    # Add more...
}

st.header(labels["Upload File"][language])
st.title("📉 Econometric Modeling")

df = st.session_state.get("df")
if df is not None:
    cols = df.select_dtypes(include='number').columns.tolist()
    y = st.selectbox("Choose dependent variable", cols)
    X = st.multiselect("Choose independent variables", [c for c in cols if c != y])

    if y and X:
        X_vars = sm.add_constant(df[X])
        model = sm.OLS(df[y], X_vars).fit()
        st.write(model.summary())
else:
    st.warning("Upload a dataset first.")
