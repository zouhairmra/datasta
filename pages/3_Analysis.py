import streamlit as st

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("🔒 Please log in to access this page.")
    st.stop()

import streamlit as st
import statsmodels.api as sm
import pandas as pd

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
