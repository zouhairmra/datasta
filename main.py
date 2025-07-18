import streamlit as st
import bcrypt

st.set_page_config(page_title="DataStatPro", layout="wide")

# Pre-hashed passwords for pass123 and guest
users = {
    "zmrabet": {
        "name": "Zouhair Mrabet",
        "password_hash": b"$2b$12$H0CcfjOxAJ6swhIqYf/k5OLwZ3Ivn/JRO9snWZaF8NFS.8fPgySya"  # pass123
    },
    "guest": {
        "name": "Guest User",
        "password_hash": b"$2b$12$7sG8mH4YtIHMTnqlZ8gkYedD3dv8muI3P/kzKfpJx9P3PKv8biuXW"  # guest
    }
}

def check_password(username, password):
    if username in users:
        return bcrypt.checkpw(password.encode(), users[username]["password_hash"])
    return False

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.name = None

if not st.session_state.logged_in:
    st.title("🔐 Login to DataStatPro")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_password(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.name = users[username]["name"]
            st.success(f"Welcome {st.session_state.name}!")
        else:
            st.error("❌ Incorrect username or password")
else:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, username=None, name=None))
    st.title(f"📊 Welcome, {st.session_state.name}!")

    st.markdown("""
    **DataStatPro** helps you upload, explore, and analyze economic & financial data easily.

    **Features:**
    - 📥 Upload your dataset
    - 📈 Perform Exploratory Data Analysis
    - 🔍 Run Econometric Models
    - 📉 Forecast with Time Series & Machine Learning
    - 🌍 Connect to World Bank datasets
    """)
