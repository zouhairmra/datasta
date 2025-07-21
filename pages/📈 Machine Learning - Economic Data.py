import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.feature_selection import SelectKBest, f_regression, chi2
import joblib

st.set_page_config(page_title="📈 Machine Learning - Economic Data", layout="wide")
st.title("📈 Machine Learning on Economic Data")

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

        if st.checkbox("🔎 Use auto-feature selection") and features:
            k = st.slider("Number of top features to select", 1, len(features), min(3, len(features)))
            selector = SelectKBest(score_func=f_regression, k=k)
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
            else:
                acc = accuracy_score(y_test, y_pred)
                st.write(f"Accuracy: {acc:.2f}")

            if st.checkbox("📊 Run cross-validation"):
                k = st.slider("Number of folds", 2, 10, 5)
                score_type = "neg_root_mean_squared_error" if problem_type == "regression" else "accuracy"
                cv_scores = cross_val_score(model, X, y, cv=k, scoring=score_type)
                mean_score = np.abs(cv_scores.mean()) if problem_type == "regression" else cv_scores.mean()
                st.write(f"Mean CV Score: {mean_score:.2f}")
                st.write("All CV Scores:", np.round(np.abs(cv_scores), 2) if problem_type == "regression" else np.round(cv_scores, 2))

            # Downloadable model
            joblib.dump(model, "trained_model.pkl")
            with open("trained_model.pkl", "rb") as f:
                st.download_button("📦 Download Trained Model", f, file_name="model.pkl")

            # Quiz section
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
