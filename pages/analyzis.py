import pandas as pd
import requests
import os
import altair as alt
import streamlit as st

# Get World Bank data via API
def  def get_world_bank_data(indicator, countries=["USA", "FRA", "QAT"], start_year=2000, end_year=2022):
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
            continue  # skip if not a proper JSON
        
        if response.status_code != 200 or len(data) < 2 or data[1] is None:
            continue

        for entry in data[1]:
            if entry["value"] is not None:
                all_data.append({
                    "country": entry["country"]["value"],
                    "date": int(entry["date"]),
                    indicator: entry["value"]
                })

    return pd.DataFrame(all_data)

        

# Save uploaded data
def save_user_data(dataframe, user_folder, filename="uploaded_data.csv"):
    os.makedirs(user_folder, exist_ok=True)
    full_path = os.path.join(user_folder, filename)
    dataframe.to_csv(full_path, index=False)
    return full_path

# Create time series chart
def plot_indicator(df, indicator):
    chart = alt.Chart(df).mark_line().encode(
        x='date:O',
        y=indicator,
        color='country:N'
    ).properties(width=700, height=400)
    return chart

# Streamlit interface
st.title("📈 World Bank Indicator Analysis")

indicator = st.selectbox("Select Indicator", {
    "GDP per capita (current US$)": "NY.GDP.PCAP.CD",
    "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
    "Life expectancy": "SP.DYN.LE00.IN",
    "Population": "SP.POP.TOTL"
})

countries = st.multiselect("Select Countries", ["USA", "FRA", "QAT", "DEU", "CHN", "IND", "BRA", "ZAF"], default=["USA", "FRA", "QAT"])
start_year = st.slider("Start Year", 1960, 2022, 2000)
end_year = st.slider("End Year", 1960, 2023, 2022)

if st.button("Fetch Data"):
    df = get_world_bank_data(indicator, countries, start_year, end_year)
    if not df.empty:
        st.write(df)
        st.altair_chart(plot_indicator(df, indicator))
    else:
        st.warning("No data found for the selected parameters.")
