import streamlit as st



import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.title("🔍 Exploratory Data Analysis")

df = st.session_state.get("df")
if df is not None:
    st.write("## Correlation Matrix")
    selected = st.multiselect("Choose variables:", df.select_dtypes(include='number').columns.tolist())
    if selected:
        corr = df[selected].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        st.pyplot(plt.gcf())
        plt.clf()
    st.write("## Descriptive Statistics", df.describe())
else:
    st.warning("Upload a dataset first.")
