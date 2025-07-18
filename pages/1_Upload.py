import streamlit as st

import streamlit as st
import pandas as pd

st.title("📥 Upload Your Dataset")
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.session_state["df"] = df
    st.write("✅ Data Preview", df.head())
