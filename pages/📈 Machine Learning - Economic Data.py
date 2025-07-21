import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.feature_selection import SelectKBest, f_regression, chi2
import shap
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import datetime

# Streamlit Page Configuration
st.set_page_config(page_title="📈 Machine Learning - Economic Data", layout="wide")
st.title("📈 Machine Learning on Economic Data")

# ---------- DATABASE CONNECTION ---------- #
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("ml_models.db", check_same_thread=False)
    return conn

conn = get_connection()
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS model_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        features TEXT,
        problem_type TEXT,
        metric_value REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def save_metrics(target, selected_features, problem_type, metric_value):
    cursor.execute(
        "INSERT INTO model_metrics (target, features, problem_type, metric_value) VALUES (?, ?, ?, ?)",
        (target, ','.join(selected_features), problem_type, metric_value)
    )
    conn.commit()

# ---------- DATA LOADING ---------- #
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("## Preview of Data")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Please upload a dataset with at least two numeric columns.")
    else:
        target = st.selectbox("🎯 Select target variable (Y)", numeric_cols)
        features = st.multiselect("🧮 Select feature variables (X)", [col for col in numeric_cols if col != target])

        if st.checkbox("🔎 Use auto-feature selection"):
            k = st.slider("Number of top features to select", 1, len(features), min(3, len(features)))
            score_func = f_regression if df[target].nunique() > 2 else chi2
            selector = SelectKBest(score_func=score_func, k=k)
            X_selected = selector.fit_transform(df[features], df[target])
            selected_features = [features[i] for i in selector.get_support(indices=True)]
            st.write("Selected Features:", selected_features)
        else:
            selected_features = features

        if selected_features:
            problem_type = st.radio("Select problem type", ["regression", "classification"])
            test_size = st.slider("Test size (%)", 10, 50, 20)

            X = df[selected_features]
            y = df[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size / 100, random_state=42)

            model = RandomForestRegressor() if problem_type == "regression" else RandomForestClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("📊 Evaluation Results")
            if problem_type == "regression":
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                st.write(f"RMSE: {rmse:.2f}")
                metric_value = rmse
            else:
                acc = accuracy_score(y_test, y_pred)
                st.write(f"Accuracy: {acc:.2f}")
                metric_value = acc

            save_metrics(target, selected_features, problem_type, metric_value)

            # Feature Importance
            st.subheader("📈 Feature Importance")
            importances = model.feature_importances_
            fig, ax = plt.subplots()
            sns.barplot(x=importances, y=selected_features, ax=ax)
            ax.set_title("Feature Importance")
            st.pyplot(fig)

            # SHAP Explainability
            st.subheader("🔍 Model Interpretability (SHAP)")
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test)
            st.write("SHAP Summary Plot:")
            shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
            st.pyplot(bbox_inches='tight')

            # Cross Validation
            if st.checkbox("📊 Run cross-validation"):
                k = st.slider("Number of folds", 2, 10, 5)
                score_type = "neg_root_mean_squared_error" if problem_type == "regression" else "accuracy"
                cv_scores = cross_val_score(model, X, y, cv=k, scoring=score_type)
                st.write(f"Mean CV Score: {np.abs(cv_scores.mean()):.2f}")
                st.write("All CV Scores:", np.round(np.abs(cv_scores), 2))

            # Download Model
            joblib.dump(model, "trained_model.pkl")
            with open("trained_model.pkl", "rb") as f:
                st.download_button("📦 Download Trained Model", f, file_name="model.pkl")

            # Prediction Quiz
            st.markdown("---")
            st.subheader("🧠 Try a Quiz: Predict the Target")
            sample = df.sample(1)
            st.write("Guess the target for this observation:")
            st.write(sample[selected_features])
            guess = st.number_input("Your guess for the target value:", format="%.2f")
            actual = sample[target].values[0]
            if st.button("Submit Guess"):
                st.success(f"Actual: {actual}, Your guess: {guess}")
                st.write(f"Error: {abs(guess - actual):.2f}")
