import streamlit as st
import streamlit_authenticator as stauth

# Configuration for authentication
config = {
    'credentials': {
        'usernames': {
            'zmrabet': {
                'name': 'Zouhair Mrabet',
                'password': stauth.Hasher(['pass123']).generate()[0]
            },
            'guest': {
                'name': 'Guest User',
                'password': stauth.Hasher(['guest']).generate()[0]
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

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.set_page_config(page_title="DataStatPro", layout="wide")
    st.title(f"📊 Welcome, {name}!")

    st.markdown("""
    **DataStatPro** helps you upload, explore, and analyze economic & financial data easily.

    **Features:**
    - 📥 Upload your dataset
    - 📈 Perform Exploratory Data Analysis
    - 🔍 Run Econometric Models
    - 📉 Forecast with Time Series & Machine Learning
    """)
elif authentication_status is False:
    st.error('Incorrect username or password')
elif authentication_status is None:
    st.warning('Please enter your username and password')
