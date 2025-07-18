import streamlit as st
import pandas as pd
import altair as alt
import requests
import datetime
import os

# -----------------------------------
# Get World Bank data for a given indicator
# -----------------------------------
def get_world_bank_data(indicator, countries=["USA", "FRA", "QAT"], start_year=2000, end_year=2022):
    all_data = []

    for country in countries:
        url = (
            f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
            f"?date={start_year}:{end_year}&format=json&per_page=10000"
        )
        response = requests.get(url)
        
        try:
            data = response.json()
        except Exception:
            st.warning(f"Failed to parse data for {country}")
            continue

        if response.status_code != 200 or len(data) < 2 or data[1] is None:
            st.warning(f"No data for {country} - indicator: {indicator}")
            continue

        for entry in data[1]:
            if entry["value"] is not None:
                all_data.append({
                    "country": entry["country"]["value"],
                    "date": int(entry["date"]),
                    indicator: entry["value"]
                })

    return pd.DataFrame(all_data)

# -----------------------------------
# Save uploaded data
# -----------------------------------
def save_user_data(dataframe, user_folder, filename="uploaded_data.csv"):
    os.makedirs(user_folder, exist_ok=True)
    full_path = os.path.join(user_folder, filename)
    dataframe.to_csv(full_path, index=False)
    return full_path

# -----------------------------------
# Create a time series chart
# -----------------------------------
def plot_indicator(df, indicator):
    chart = alt.Chart(df).mark_line().encode(
        x='date:O',
        y=indicator,
        color='country'
    ).properties(width=700, height=400)
    return chart

# -----------------------------------
# Streamlit UI
# -----------------------------------
st.title("📈 World Bank Economic Data Analysis")

st.markdown("Analyze World Bank data by selecting an indicator, countries, and time range.")

with st.form("form"):
    indicator = st.text_input("World Bank Indicator Code", "NY.GDP.PCAP.CD")
    countries_input = st.text_input("Country ISO codes (comma-separated)", "USA,FRA,QAT")
    countries = [c.strip().upper() for c in countries_input.split(",") if c.strip()]
    start_year = st.number_input("Start Year", min_value=1960, max_value=2023, value=2000)
    end_year = st.number_input("End Year", min_value=1960, max_value=2023, value=2022)
    submit = st.form_submit_button("Fetch Data")

if submit:
    with st.spinner("Fetching data from World Bank..."):
        df = get_world_bank_data(indicator, countries, start_year, end_year)
        if df.empty:
            st.error("No data retrieved. Please check the indicator code or countries.")
        else:
            st.success(f"Retrieved {len(df)} rows of data.")
            st.dataframe(df)
            st.altair_chart(plot_indicator(df, indicator), use_container_width=True)
