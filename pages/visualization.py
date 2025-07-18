import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Example function to run ARIMA
def run_arima_model(df, target_col):
    model = auto_arima(df[target_col], seasonal=False, trace=True)
    forecast = model.predict(n_periods=10)
    return forecast

# Streamlit UI
st.title("ARIMA Forecast Example")

uploaded_file = st.file_uploader("Upload your time series CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Data preview:", df.head())

    target_col = st.selectbox("Select column for ARIMA model", df.columns)

    if st.button("Run ARIMA Forecast"):
        try:
            forecast = run_arima_model(df, target_col)
            st.write("Forecast:", forecast)

            fig, ax = plt.subplots()
            df[target_col].plot(ax=ax, label='Original')
            pd.Series(forecast).plot(ax=ax, label='Forecast')
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error in ARIMA modeling: {e}")
