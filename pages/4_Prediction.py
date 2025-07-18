import streamlit as st

if 'authentication_status' not in st.session_state or not st.session_state.authentication_status:
    st.warning("🔒 Please log in to access this page.")
    st.stop()

import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("🤖 Forecasting (Beta)")

df = st.session_state.get("df")
if df is not None:
    target = st.selectbox("Select variable to forecast", df.select_dtypes(include='number').columns)
    steps = st.slider("Forecast steps", 1, 20, 5)

    if target:
        y = df[target].dropna().values.reshape(-1, 1)
        X = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression().fit(X, y)
        future = model.predict(np.arange(len(y), len(y)+steps).reshape(-1, 1))

        st.line_chart(np.concatenate([y, future]))
else:
    st.warning("Upload a dataset first.")
