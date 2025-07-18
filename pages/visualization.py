import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

st.set_page_config(page_title="Modeling", layout="wide")
st.title("📈 Modeling & Statistical Analysis")

st.sidebar.subheader("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    (
        "Descriptive Statistics",
        "Inferential Statistics",
        "Correlation Analysis",
        "Data Visualization",
        "Advanced Modeling"
    )
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    if analysis_type == "Descriptive Statistics":
        st.header("Descriptive Statistics")
        st.write(df.describe())

    elif analysis_type == "Inferential Statistics":
        st.header("Inferential Statistics (T-Test)")
        if len(numeric_cols) >= 2:
            col1 = st.selectbox("Select First Variable", numeric_cols)
            col2 = st.selectbox("Select Second Variable", [col for col in numeric_cols if col != col1])
            test_type = st.radio("Test Type", ["Independent t-test", "Paired t-test"])
            if st.button("Run T-Test"):
                from scipy import stats
                try:
                    if test_type == "Independent t-test":
                        stat, p = stats.ttest_ind(df[col1].dropna(), df[col2].dropna())
                    else:
                        stat, p = stats.ttest_rel(df[col1].dropna(), df[col2].dropna())
                    st.write(f"**T-statistic:** {stat:.4f}")
                    st.write(f"**P-value:** {p:.4f}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("At least two numeric columns are required.")

    elif analysis_type == "Correlation Analysis":
        st.header("Correlation Analysis")
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Need at least two numeric columns.")

    elif analysis_type == "Data Visualization":
        st.header("Data Visualization")
        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Histogram", "Boxplot", "Scatterplot", "Lineplot", "Pie Chart"]
        )

        if chart_type == "Histogram":
            col = st.selectbox("Select Numeric Variable", numeric_cols)
            bins = st.slider("Number of Bins", 5, 100, 20)
            fig, ax = plt.subplots()
            sns.histplot(df[col], bins=bins, kde=True, ax=ax)
            st.pyplot(fig)

        elif chart_type == "Boxplot":
            col = st.selectbox("Select Numeric Variable", numeric_cols)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[col], ax=ax)
            st.pyplot(fig)

        elif chart_type == "Scatterplot":
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x], y=df[y], ax=ax)
            sns.regplot(x=df[x], y=df[y], ax=ax, scatter=False, color='red')
            st.pyplot(fig)

        elif chart_type == "Lineplot":
            x = st.selectbox("X-axis (e.g., Year)", numeric_cols)
            y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
            fig, ax = plt.subplots()
            sns.lineplot(x=df[x], y=df[y], ax=ax)
            st.pyplot(fig)

        elif chart_type == "Pie Chart":
            if len(categorical_cols) > 0:
                cat_col = st.selectbox("Select Categorical Column", categorical_cols)
                value_counts = df[cat_col].value_counts()
                fig, ax = plt.subplots()
                ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.warning("No categorical columns available for pie chart.")

    elif analysis_type == "Advanced Modeling":
        st.header("📉 Advanced Modeling")

        model_type = st.selectbox(
            "Select Model Type",
            ["Linear Regression", "ARIMA", "SARIMA", "Auto ARIMA"]
        )

        if model_type == "Linear Regression":
            x = st.selectbox("Independent Variable", numeric_cols)
            y = st.selectbox("Dependent Variable", [col for col in numeric_cols if col != x])

            X = df[[x]].dropna()
            y_vals = df[y].dropna()
            if len(X) == len(y_vals):
                model = LinearRegression().fit(X, y_vals)
                y_pred = model.predict(X)

                fig, ax = plt.subplots()
                ax.scatter(X, y_vals, label='Actual')
                ax.plot(X, y_pred, color='red', label='Regression Line')
                ax.set_xlabel(x)
                ax.set_ylabel(y)
                ax.legend()
                st.pyplot(fig)

                st.write(f"**Intercept:** {model.intercept_:.4f}")
                st.write(f"**Slope:** {model.coef_[0]:.4f}")
                st.write(f"**R²:** {model.score(X, y_vals):.4f}")
            else:
                st.error("Mismatch in data lengths. Please check for missing values.")

        elif model_type in ["ARIMA", "SARIMA", "Auto ARIMA"]:
            ts_col = st.selectbox("Select Time Series Column", numeric_cols)
            st.write("⚠️ Ensure the data is sorted by time and missing values are handled.")
            data = df[ts_col].dropna()

            if model_type == "ARIMA":
                p = st.slider("AR order (p)", 0, 5, 1)
                d = st.slider("Differencing order (d)", 0, 2, 1)
                q = st.slider("MA order (q)", 0, 5, 1)
                model = ARIMA(data, order=(p, d, q))
                results = model.fit()
                forecast = results.forecast(10)
                st.write(results.summary())

            elif model_type == "SARIMA":
                p = st.slider("AR (p)", 0, 2, 1)
                d = st.slider("I (d)", 0, 1, 1)
                q = st.slider("MA (q)", 0, 2, 1)
                P = st.slider("Seasonal AR (P)", 0, 2, 1)
                D = st.slider("Seasonal I (D)", 0, 1, 1)
                Q = st.slider("Seasonal MA (Q)", 0, 2, 1)
                s = st.slider("Seasonal Period (s)", 1, 12, 4)
                model = SARIMAX(data, order=(p, d, q), seasonal_order=(P, D, Q, s))
                results = model.fit()
                forecast = results.forecast(10)
                st.write(results.summary())

            elif model_type == "Auto ARIMA":
                stepwise = st.checkbox("Use stepwise", value=True)
                suppress = st.checkbox("Suppress Warnings", value=True)
                model = auto_arima(data, seasonal=False, stepwise=stepwise, suppress_warnings=suppress)
                forecast = model.predict(n_periods=10)
                st.write(model.summary())

            # Plot original and forecast
            fig, ax = plt.subplots()
            data.plot(label="Original", ax=ax)
            pd.Series(forecast, index=range(len(data), len(data) + len(forecast))).plot(label="Forecast", ax=ax)
            plt.legend()
            st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to begin.")

