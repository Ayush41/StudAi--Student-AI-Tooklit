import streamlit as st
import requests
import json
import uuid
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = ""
SUPABASE_KEY = ""
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Webhook URL
WEBHOOK_URL = ""

def generate_session_id():
    return str(uuid.uuid4())

def init_session_state():
    if "auth" not in st.session_state:
        st.session_state.auth = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])