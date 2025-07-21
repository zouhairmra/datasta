import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

st.title("📈 Machine Learning on Economic Data")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:", df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("You need at least 2 numeric columns to proceed.")
    else:
        x_var = st.selectbox("Select feature (X)", options=numeric_cols)
        y_var = st.selectbox("Select target (y)", options=[col for col in numeric_cols if col != x_var])

        X = df[[x_var]]
        y = df[y_var]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        st.write(f"**RMSE:** {rmse:.2f}")
