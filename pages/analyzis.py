import streamlit as st
import pandas as pd
import altair as alt
import requests
import io

# -----------------------------------
# World Bank utility functions
# -----------------------------------

@st.cache_data
def get_all_countries():
    countries = []
    url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for c in data[1]:
            if c["region"]["value"] != "Aggregates":
                countries.append(c["id"])
    return countries

def get_world_bank_data(indicators, countries, start_year=1960, end_year=2025):
    full_df = pd.DataFrame()

    for indicator in indicators:
        for country in countries:
            url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json&per_page=10000"
            response = requests.get(url)

            try:
                data = response.json()
            except Exception:
                st.warning(f"Cannot decode JSON for {country} - {indicator}")
                continue

            if response.status_code != 200 or len(data) < 2 or data[1] is None:
                continue

            for record in data[1]:
                if record["value"] is not None:
                    full_df = pd.concat([
                        full_df,
                        pd.DataFrame([{
                            "country": record["country"]["value"],
                            "country_code": record["country"]["id"],
                            "date": int(record["date"]),
                            "indicator": indicator,
                            "value": record["value"]
                        }])
                    ], ignore_index=True)

    return full_df

def prepare_pivot_table(df):
    pivot_df = df.pivot_table(index=["country", "date"], columns="indicator", values="value").reset_index()
    return pivot_df

def plot_data(df, indicator):
    chart = alt.Chart(df).mark_line().encode(
        x='date:O',
        y=indicator,
        color='country'
    ).properties(width=800, height=450)
    return chart

# -----------------------------------
# Streamlit App
# -----------------------------------

st.title("🌍 World Bank Multi-Indicator Dashboard")
st.markdown("Explore multiple World Bank indicators for all countries (1960–2025).")

default_indicators = ["NY.GDP.PCAP.CD", "SP.POP.TOTL", "SE.XPD.TOTL.GD.ZS"]

with st.form("wb_form"):
    indicators = st.text_input("Indicator Codes (comma-separated)", ", ".join(default_indicators)).split(",")
    indicators = [i.strip() for i in indicators if i.strip()]
    start_year = st.number_input("Start Year", 1960, 2025, 2000)
    end_year = st.number_input("End Year", 1960, 2025, 2022)
    selected_countries = st.multiselect("Countries (leave blank for all)", options=get_all_countries())
    submit = st.form_submit_button("Fetch World Bank Data")

if submit:
    st.info("Fetching data from World Bank. This may take a few minutes...")
    countries = selected_countries if selected_countries else get_all_countries()
    data = get_world_bank_data(indicators, countries, start_year, end_year)

    if data.empty:
        st.error("No data was retrieved.")
    else:
        st.success(f"Retrieved {len(data)} data points.")
        st.dataframe(data.head(100))

        # 📥 CSV download
        csv_data = data.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Data as CSV",
            data=csv_data,
            file_name="world_bank_data.csv",
            mime="text/csv"
        )

        pivot = prepare_pivot_table(data)
        selected_ind = st.selectbox("Select indicator to visualize", indicators)
        if selected_ind in pivot.columns:
            st.altair_chart(plot_data(pivot.dropna(subset=[selected_ind]), selected_ind), use_container_width=True)
        else:
            st.warning("No data available for the selected indicator.")
