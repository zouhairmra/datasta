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

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Encode categoricals
    label_encoders = {}
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("The dataset must contain at least 2 numeric columns.")
    else:
        x_var = st.selectbox("Select the input feature (X)", options=numeric_cols)
        y_var = st.selectbox("Select the target variable (y)", options=[col for col in numeric_cols if col != x_var])

        X = df[[x_var]]
        y = df[y_var]

        # Auto-detect problem type
        problem_type = "classification" if y.nunique() <= 10 and y.dtype in [np.int64, np.int32] else "regression"
        st.markdown(f"**Problem Type Detected:** `{problem_type.title()}`")

        # Model selection
        if problem_type == "regression":
            model_name = st.selectbox("Choose a model", ["Linear Regression", "Decision Tree", "Random Forest", "KNN"])
        else:
            model_name = st.selectbox("Choose a model", ["Logistic Regression", "Decision Tree", "Random Forest", "KNN"])

        # Train/Test Split
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
                model = LogisticRegression()
            elif model_name == "Decision Tree":
                model = DecisionTreeClassifier()
            elif model_name == "Random Forest":
                model = RandomForestClassifier()
            else:
                model = KNeighborsClassifier()

        # Train and predict
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        st.subheader("📉 Evaluation")

        if problem_type == "regression":
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            st.write(f"**RMSE:** {rmse:.2f}")
        else:
            acc = accuracy_score(y_test, y_pred)
            st.write(f"**Accuracy:** {acc*100:.2f}%")

        # Optional: Plotting results
        st.subheader("📈 Prediction Plot")
        fig, ax = plt.subplots()
        if problem_type == "regression":
            sns.scatterplot(x=y_test, y=y_pred, ax=ax)
            ax.set_xlabel("Actual")
            ax.set_ylabel("Predicted")
        else:
            sns.histplot(y_pred, kde=True, ax=ax)
            ax.set_xlabel("Predicted Labels")
        st.pyplot(fig)
