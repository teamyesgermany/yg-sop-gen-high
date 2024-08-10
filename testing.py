import streamlit as st
import pyrebase
import warnings
from datetime import datetime, timedelta
from streamlit_cookies_manager import EncryptedCookieManager
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Your Diffbot API token
PYREBASE_API_KEY = os.getenv("PYREBASE_API_KEY")

# Turn Streamlit's st.cache deprecation warnings into exceptions
warnings.filterwarnings("error", message=".*st.cache is deprecated.*")

try:
    # Your code that might cause the deprecation warning
    # Initialize Firebase
    firebaseConfig = {
        'apiKey': f"{PYREBASE_API_KEY}",
        'authDomain': "yg-sop-gen-high.firebaseapp.com",
        'projectId': "yg-sop-gen-high",
        'databaseURL': "https://yg-sop-gen-high-default-rtdb.firebaseio.com/",
        'storageBucket': "yg-sop-gen-high.appspot.com",
        'messagingSenderId': "912444145418",
        'appId': "1:912444145418:web:d157bb3a58a1176de704f3",
        'measurementId': "G-6BXXTL8T1L"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    # Initialize the cookie manager
    cookies = EncryptedCookieManager(password="your-secure-password")

    # Ensure cookies are ready before proceeding
    if not cookies.ready():
        st.stop()  # Stop the script until the cookies are ready

    # Check if the user is already logged in via cookies
    if "logged_in" not in st.session_state:
        logged_in_cookie = cookies.get("logged_in")
        st.session_state.logged_in = logged_in_cookie == "true"
        st.session_state.user_email = cookies.get("user_email") if st.session_state.logged_in else None

    if not st.session_state.logged_in:
        # Login form
        email = st.text_input('Please enter your email address')
        password = st.text_input('Please enter your password', type='password')

        if st.button('Login'):
            try:
                # Sign in with Firebase
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.logged_in = True
                st.session_state.user_email = user['email']

                # Set cookies to persist the login state for 24 hours
                expires_at = (datetime.now() + timedelta(seconds=60)).isoformat()
                cookies["logged_in"] = "true"
                cookies["user_email"] = user['email']
                cookies["expires_at"] = expires_at
                cookies.save()

                st.success('Logged in successfully!')
                st.experimental_rerun()  # Refresh the page to show the main content
            except Exception as e:
                st.error(f"Login failed: {e}")
    else:
        # Main application content
        st.markdown("# 📝 YESGEN AI")
        st.write(f"Welcome, {st.session_state.user_email}!")
        # Add a logout button
        if st.button('Logout'):
            # Clear session state
            st.session_state.logged_in = False
            st.session_state.user_email = None

            # Delete the cookies to log out
            del cookies["logged_in"]
            del cookies["user_email"]
            del cookies["expires_at"]
            cookies.save()

            st.experimental_rerun()  # Refresh the page to show the login screen

except UserWarning as e:
    st.error(f"An exception occurred: {e}")
    st.stop()  # Stop the script if this specific deprecation warning occurs
