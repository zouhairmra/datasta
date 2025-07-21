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
        problem_type = st.radio("Select problem type", ["regression", "classification"])
        features = st.multiselect("🧮 Select feature variables (X)", [col for col in numeric_cols if col != target])

        selected_features = []

        if features:
            if st.checkbox("🔎 Use auto-feature selection"):
                k = st.slider("Number of top features to select", 1, len(features), min(3, len(features)))
                score_func = f_regression if problem_type == "regression" else chi2
                X_for_selection = df[features]
                y_for_selection = df[target]

                # For chi2, all values must be non-negative
                if problem_type == "classification":
                    X_for_selection = X_for_selection - X_for_selection.min()

                selector = SelectKBest(score_func=score_func, k=k)
                X_selected = selector.fit_transform(X_for_selection, y_for_selection)
                selected_features = [features[i] for i in selector.get_support(indices=True)]
                st.write("Selected Features:", selected_features)
            else:
                selected_features = features

        if selected_features:
            test_size = st.slider("Test size (%)", 10, 50, 20)

            X = df[selected_features]
            y = df[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size / 100, random_state=42)

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
                st.write(f"RMSE: {rmse:.2f}")
            else:
                st.write(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

            if st.checkbox("📊 Run cross-validation"):
                k = st.slider("Number of folds", 2, 10, 5)
                score_type = "neg_root_mean_squared_error" if problem_type == "regression" else "accuracy"
                cv_scores = cross_val_score(model, X, y, cv=k, scoring=score_type)
                st.write(f"Mean CV Score: {np.abs(cv_scores.mean()):.2f}")
                st.write("All CV Scores:", np.round(np.abs(cv_scores), 2))

            joblib.dump(model, "trained_model.pkl")
            with open("trained_model.pkl", "rb") as f:
                st.download_button("📦 Download Trained Model", f, file_name="model.pkl")

            st.markdown("---")
            st.subheader("🧠 Try a Quiz: Predict the Target")
            sample = df.sample(1)
            st.write("Guess the target for this observation:")
            st.write(sample[selected_features])

            if problem_type == "regression":
                guess = st.number_input("Your guess for the target value:", format="%.2f")
                actual = sample[target].values[0]
                if st.button("Submit Guess"):
                    st.success(f"Actual: {actual}, Your guess: {guess}")
                    st.write(f"Error: {abs(guess - actual):.2f}")
            else:
                options = df[target].unique().tolist()
                guess = st.selectbox("Your guess for the target class:", options)
                actual = sample[target].values[0]
                if st.button("Submit Guess"):
                    if guess == actual:
                        st.success(f"Correct! 🎉 It was {actual}")
                    else:
                        st.error(f"Incorrect. You guessed {guess}, but actual was {actual}")
