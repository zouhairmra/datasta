import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier, XGBRegressor
from sqlalchemy import create_engine

# === DATABASE CONNECTION ===
@st.cache_resource
def get_engine():
    db_url = st.secrets["database"]["url"]
    return create_engine(db_url)

# === PAGE TITLE ===
st.title("📈 Machine Learning - Economic Data")

# === DATA UPLOAD ===
uploaded_file = st.file_uploader("Upload your economic dataset (CSV format)", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview:")
    st.dataframe(data.head())

    # === FEATURE SELECTION ===
    all_columns = data.columns.tolist()
    target_column = st.selectbox("Select target variable", all_columns)
    feature_columns = st.multiselect("Select features", [col for col in all_columns if col != target_column])

    if st.button("Train Model") and target_column and feature_columns:
        df = data[feature_columns + [target_column]].dropna()

        # Encode categoricals
        for col in df.select_dtypes(include=['object', 'category']).columns:
            df[col] = LabelEncoder().fit_transform(df[col])

        X = df[feature_columns]
        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # === MODEL SELECTION ===
        model_choice = st.selectbox("Select model", ["Random Forest", "XGBoost", "SVM"])

        if model_choice == "Random Forest":
            model = RandomForestRegressor()
        elif model_choice == "XGBoost":
            model = XGBRegressor()
        else:
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            model = SVC()

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if len(np.unique(y)) > 10:  # Regression
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            st.write(f"RMSE: {rmse:.2f}")
        else:  # Classification
            acc = accuracy_score(y_test, y_pred)
            st.write(f"Accuracy: {acc:.2f}")

        # === CHARTS ===
        st.subheader("Feature Importance")
        explainer = shap.Explainer(model, X_train)
        shap_values = explainer(X_test)
        st.set_option('deprecation.showPyplotGlobalUse', True)
        shap.summary_plot(shap_values, X_test, show=False)
        st.pyplot(bbox_inches='tight')

        # === SAVE TO DATABASE ===
        save_to_db = st.checkbox("Save results to database")
        if save_to_db:
            engine = get_engine()
            result_df = pd.DataFrame({"y_test": y_test, "y_pred": y_pred})
            result_df.to_sql("ml_results", con=engine, if_exists="replace", index=False)
            st.success("Results saved to the database.")
