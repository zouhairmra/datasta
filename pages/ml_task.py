import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Predict Economic Indicators with Machine Learning")

uploaded_file = st.file_uploader("Upload your CSV dataset", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📊 Data Preview", df.head())

    features = st.multiselect("🧮 Select Feature Columns (X)", df.columns)
    target = st.selectbox("🎯 Select Target Column (y)", df.columns)

    if features and target:
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model_name = st.selectbox("🤖 Choose a Model", ["Linear Regression", "Random Forest", "Ridge Regression"])
        if model_name == "Linear Regression":
            model = LinearRegression()
        elif model_name == "Random Forest":
            model = RandomForestRegressor()
        else:
            model = Ridge()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        st.write(f"📉 Mean Squared Error: {mse:.2f}")

        if model_name == "Random Forest":
            fig, ax = plt.subplots()
            ax.barh(features, model.feature_importances_)
            ax.set_title("Feature Importances")
            st.pyplot(fig)
        elif hasattr(model, "coef_"):
            st.write("📌 Coefficients:", model.coef_)

        # Download button
        results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
        csv = results.to_csv(index=False).encode()
        st.download_button("⬇️ Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")

