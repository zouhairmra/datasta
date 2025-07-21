import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Machine Learning on Economic Data")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    df.dropna(inplace=True)

    # Encode categorical variables
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("The dataset must contain at least 2 numeric columns.")
    else:
        target = st.selectbox("🎯 Select the target variable (y)", options=numeric_cols)
        features = st.multiselect("🧮 Select input features (X)", options=[col for col in numeric_cols if col != target])

        if features:
            X = df[features]
            y = df[target]

            # Auto-detect classification vs regression
            problem_type = "classification" if y.nunique() <= 10 and y.dtype in [np.int64, np.int32] else "regression"
            st.markdown(f"**Detected Problem Type:** `{problem_type.title()}`")

            # Model selection
            if problem_type == "regression":
                model_name = st.selectbox("Choose a regression model", ["Linear Regression", "Decision Tree", "Random Forest", "KNN"])
            else:
                model_name = st.selectbox("Choose a classification model", ["Logistic Regression", "Decision Tree", "Random Forest", "KNN"])

            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Model initialization
            if problem_type == "regression":
                if model_name == "Linear Regression":
                    model = LinearRegression()
                elif model_name == "Decision Tree":
                    model = DecisionTreeRegressor()
                elif model_name == "Random Forest":
                    model = RandomForestRegressor()
                else:
                    model = KNeighborsRegressor()
            else:
                if model_name == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000)
                elif model_name == "Decision Tree":
                    model = DecisionTreeClassifier()
                elif model_name == "Random Forest":
                    model = RandomForestClassifier()
                else:
                    model = KNeighborsClassifier()

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("📉 Model Evaluation")
            if problem_type == "regression":
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                st.write(f"**RMSE:** {rmse:.2f}")
            else:
                accuracy = accuracy_score(y_test, y_pred)
                st.write(f"**Accuracy:** {accuracy * 100:.2f}%")

            # Feature importance (if available)
            if hasattr(model, "feature_importances_"):
                st.subheader("🔍 Feature Importance")
                importance = pd.DataFrame({
                    "Feature": features,
                    "Importance": model.feature_importances_
                }).sort_values(by="Importance", ascending=False)
                st.dataframe(importance)

                fig, ax = plt.subplots()
                sns.barplot(x="Importance", y="Feature", data=importance, ax=ax)
                st.pyplot(fig)

            elif hasattr(model, "coef_"):
                st.subheader("📈 Coefficients")
                coef = pd.DataFrame({
                    "Feature": features,
                    "Coefficient": model.coef_.flatten() if model.coef_.ndim > 1 else model.coef_
                }).sort_values(by="Coefficient", key=abs, ascending=False)
                st.dataframe(coef)

                fig, ax = plt.subplots()
                sns.barplot(x="Coefficient", y="Feature", data=coef, ax=ax)
                st.pyplot(fig)

            # Prediction results preview
            st.subheader("📋 Predictions vs Actuals")
            result_df = pd.DataFrame({
                "Actual": y_test,
                "Predicted": y_pred
            }).reset_index(drop=True)
            st.dataframe(result_df.head())

