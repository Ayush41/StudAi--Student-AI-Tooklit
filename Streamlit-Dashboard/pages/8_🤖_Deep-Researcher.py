import streamlit as st
from utils.auth import check_auth, show_login_page

if not check_auth():
    show_login_page()
    st.stop()  # Prevent access to the feature
    
# Rest of your feature page code...