import streamlit as st
import streamlit_authenticator as stauth

# Page configuration
st.set_page_config(page_title="DataStatPro", layout="wide")

# User credentials with pre-hashed passwords
config = {
    'credentials': {
        'usernames': {
            'zmrabet': {
                'name': 'Zouhair Mrabet',
                'password': '$2b$12$H0CcfjOxAJ6swhIqYf/k5OLwZ3Ivn/JRO9snWZaF8NFS.8fPgySya'  # pass123
            },
            'guest': {
                'name': 'Guest User',
                'password': '$2b$12$7sG8mH4YtIHMTnqlZ8gkYedD3dv8muI3P/kzKfpJx9P3PKv8biuXW'  # guest
            }
        }
    },
    'cookie': {
        'name': 'datastatpro-cookie',
        'key': 'abcdef123456',
        'expiry_days': 1
    },
    'preauthorized': {
        'emails': []
    }
}

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Login call - keyword argument for location
name, authentication_status, username = authenticator.login('Login', location='main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.title(f"📊 Welcome, {name}!")

    st.markdown("""
    **DataStatPro** helps you upload, explore, and analyze economic & financial data easily.

    **Features:**
    - 📥 Upload your dataset
    - 📈 Perform Exploratory Data Analysis
    - 🔍 Run Econometric Models
    - 📉 Forecast with Time Series & Machine Learning
    - 🌍 Connect to World Bank datasets
    """)
elif authentication_status is False:
    st.error('❌ Incorrect username or password')
else:
    st.warning('🕵️ Please enter your username and password')
