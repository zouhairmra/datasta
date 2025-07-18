import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Page title
st.set_page_config(page_title="Modeling", layout="wide")
st.title("📊 Modeling & Statistical Analysis")

# Sidebar - file uploader and analysis options
st.sidebar.subheader("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

analysis_type = st.sidebar.radio(
    "Select Analysis Type",
    ("Descriptive Statistics", "Inferential Statistics", "Correlation Analysis", "Data Visualization")
)

# If a file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()

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
                try:
                    if test_type == "Independent t-test":
                        stat, p = stats.ttest_ind(df[col1].dropna(), df[col2].dropna())
                    else:
                        stat, p = stats.ttest_rel(df[col1].dropna(), df[col2].dropna())
                    st.write(f"**T-statistic:** {stat:.4f}")
                    st.write(f"**P-value:** {p:.4f}")
                    if p < 0.05:
                        st.success("Statistically significant (p < 0.05).")
                    else:
                        st.info("Not statistically significant (p ≥ 0.05).")
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
        chart_type = st.selectbox("Choose Chart Type", ["Histogram", "Boxplot", "Scatterplot", "Lineplot"])

        if chart_type == "Histogram":
            col = st.selectbox("Select Variable", numeric_cols)
            bins = st.slider("Number of Bins", 5, 100, 20)
            fig, ax = plt.subplots()
            sns.histplot(df[col], bins=bins, kde=True, ax=ax)
            st.pyplot(fig)

        elif chart_type == "Boxplot":
            col = st.selectbox("Select Variable", numeric_cols)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[col], ax=ax)
            st.pyplot(fig)

        elif chart_type == "Scatterplot":
            x = st.selectbox("X-axis", numeric_cols)
            y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x], y=df[y], ax=ax)
            st.pyplot(fig)

        elif chart_type == "Lineplot":
            x = st.selectbox("X-axis (e.g., Year)", numeric_cols)
            y = st.selectbox("Y-axis", [col for col in numeric_cols if col != x])
            fig, ax = plt.subplots()
            sns.lineplot(x=df[x], y=df[y], ax=ax)
            st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to begin.")
