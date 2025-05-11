import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def check_auth():
    """Check if user is authenticated"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check if there's a valid session
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            st.session_state.user = user.user
    except:
        st.session_state.user = None
    
    return st.session_state.user is not None

def sign_up(email, password):
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        if user and user.user:
            st.session_state.user = user.user
            return True
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return False

def sign_in(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user and user.user:
            st.session_state.user = user.user
            return True
    except Exception as e:
        st.error(f"Login failed: {e}")
        return False

def sign_out():
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

def show_login_page():
    st.title("🔐 Login to Your Account")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if sign_in(email, password):
                st.success("Login successful!")
                st.rerun()
    
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create Account"):
            if sign_up(email, password):
                st.success("Account created successfully! Please login.")