import streamlit as st
import bcrypt

st.set_page_config(page_title="DataStatPro", layout="wide")

# Plain passwords (only for demo; in production use hashed)
user_passwords = {
    "zmrabet": "pass123",
    "guest": "guest"
}

# On app start, hash passwords and store in dict
if "password_hashes" not in st.session_state:
    st.session_state.password_hashes = {
        user: bcrypt.hashpw(pw.encode(), bcrypt.gensalt()) for user, pw in user_passwords.items()
    }

def check_password(username, password):
    if username in st.session_state.password_hashes:
        return bcrypt.checkpw(password.encode(), st.session_state.password_hashes[username])
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
            st.session_state.name = username  # or use a dict for nicer names
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

