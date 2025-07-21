import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

st.title("📈 Machine Learning - Economic Data")

uploaded_file = st.file_uploader("Upload your economic dataset (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of dataset:")
    st.dataframe(df)

    target = st.selectbox("Select the target variable", df.columns)
    features = st.multiselect("Select feature variables", [col for col in df.columns if col != target])

    if st.button("Run Linear Regression") and target and features:
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.subheader("🔍 Results")
        st.write(f"R² score: {r2_score(y_test, y_pred):.2f}")
        st.write(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.2f}")

        st.subheader("📊 Coefficients")
        coeff_df = pd.DataFrame({"Feature": features, "Coefficient": model.coef_})
        st.dataframe(coeff_df)
