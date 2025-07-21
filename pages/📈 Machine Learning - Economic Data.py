import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_regression, chi2
from sklearn.metrics import (
    mean_squared_error,
    accuracy_score,
    confusion_matrix
)

# --- Page setup
st.set_page_config(page_title="📈 Machine Learning - Economic Data", layout="wide")
st.title("📈 Machine Learning on Economic Data")

# --- Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("## Preview of Data")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("Please upload a dataset with at least two numeric columns.")
    else:
        target = st.selectbox("🎯 Select target variable (Y)", numeric_cols)
        features = st.multiselect("🧮 Select feature variables (X)", [col for col in numeric_cols if col != target])

        selected_features = features
        if features:
            if st.checkbox("🔎 Use auto-feature selection"):
                k = st.slider("Number of top features to select", 1, len(features), min(3, len(features)))
                score_func = f_regression
                try:
                    selector = SelectKBest(score_func=score_func, k=k)
                    X_selected = selector.fit_transform(df[features], df[target])
                    selected_features = [features[i] for i in selector.get_support(indices=True)]
                    st.success(f"Selected Features: {selected_features}")
                except Exception as e:
                    st.error(f"Feature selection failed: {e}")

        if selected_features:
            problem_type = st.radio("Select problem type", ["regression", "classification"])
            test_size = st.slider("Test size (%)", 10, 50, 20)

            X = df[selected_features]
            y = df[target]

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size / 100, random_state=42
            )

            # Model selection
            if problem_type == "regression":
                model = RandomForestRegressor()
            else:
                model = RandomForestClassifier()

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("📊 Evaluation Results")
            if problem_type == "regression":
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)
                st.write(f"**RMSE:** {rmse:.2f}")
            else:
                st.write(f"**Accuracy:** {accuracy_score(y_test, y_pred):.2f}")

            # Cross-validation
            if st.checkbox("📊 Run cross-validation"):
                k = st.slider("Number of folds", 2, 10, 5)
                score_type = "neg_root_mean_squared_error" if problem_type == "regression" else "accuracy"
                cv_scores = cross_val_score(model, X, y, cv=k, scoring=score_type)
                st.write(f"**Mean CV Score:** {np.abs(cv_scores.mean()):.2f}")
                st.write("All CV Scores:", np.round(np.abs(cv_scores), 2))

            # Save/download model
            joblib.dump(model, "trained_model.pkl")
            with open("trained_model.pkl", "rb") as f:
                st.download_button("📦 Download Trained Model", f, file_name="model.pkl")

            # 📉 Charts section
            st.subheader("📉 Visualizations")

            # Feature importance
            if hasattr(model, 'feature_importances_'):
                st.write("### 🔍 Feature Importance")
                importance = model.feature_importances_
                imp_df = pd.DataFrame({'Feature': selected_features, 'Importance': importance})
                imp_df = imp_df.sort_values("Importance", ascending=False)

                fig2, ax2 = plt.subplots()
                sns.barplot(x="Importance", y="Feature", data=imp_df, ax=ax2)
                ax2.set_title("Feature Importance")
                st.pyplot(fig2)

            # Prediction vs Actual
            if problem_type == "regression":
                st.write("### 📊 Actual vs Predicted")
                fig1, ax1 = plt.subplots()
                ax1.scatter(y_test, y_pred, alpha=0.6)
                ax1.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
                ax1.set_xlabel("Actual")
                ax1.set_ylabel("Predicted")
                ax1.set_title("Actual vs Predicted")
                st.pyplot(fig1)
            else:
                st.write("### 🧮 Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred, labels=np.unique(y))
                fig3, ax3 = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=np.unique(y), yticklabels=np.unique(y), ax=ax3)
                ax3.set_xlabel("Predicted")
                ax3.set_ylabel("Actual")
                ax3.set_title("Confusion Matrix")
                st.pyplot(fig3)

            # 🎯 Prediction quiz
            st.markdown("---")
            st.subheader("🧠 Try a Quiz: Predict the Target")
            sample = df.sample(1)
            st.write("Guess the target for this observation:")
            st.write(sample[selected_features])
            guess = st.number_input("Your guess for the target value:", format="%.2f")
            actual = sample[target].values[0]
            if st.button("Submit Guess"):
                if problem_type == "regression":
                    st.success(f"Actual: {actual}, Your guess: {guess}")
                    st.write(f"Error: {abs(guess - actual):.2f}")
                else:
                    st.success(f"Actual class: {actual}")
                    st.info("This quiz is more educational for regression tasks.")
