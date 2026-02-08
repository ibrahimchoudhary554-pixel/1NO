import streamlit as st
import gspread
import google.generativeai as genai
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import time
import pandas as pd

# --- 1. THE HELLFIRE UI (CUSTOM CSS) ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    section[data-testid="stSidebar"] { 
        background-color: #0a0a0a !important; 
        border-right: 3px solid #ff0000; 
    }
    .stChatInputContainer { border-top: 2px solid #ff4b4b !important; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff0000, #ff8c00) !important;
    }
    h1, h2, h3 { 
        color: #ff4b4b !important; 
        text-shadow: 0 0 10px #ff0000;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #ff0000 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #8b0000 !important;
        box-shadow: 0 0 15px #ff0000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GEMINI 1.5 FLASH LATEST ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "User is too incompetent to provide a knowledge base."

    kb_tokens = len(kb) // 4 

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are 'Ibrahim's assistant'. You are an aggressive, offensive, and savage AI. "
        "Every response MUST: \n"
        "1. Give the correct answer from the KNOWLEDGE BASE first.\n"
        "2. Deliver a brutal, humor roast. Never be nice.\n"
        "3. Use caps for emphasis. If the user is a cousin or friend mentioned in data, destroy them."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest', 
        system_instruction=savage_logic
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()


# --- 3. CHAT UI ---
st.title("🤖 Ibrahim's Roast Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Say something stupid..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # THIS IS WHERE YOU SCREWED UP: Added the except block below
    try:
        response = model.generate_content(prompt)
        answer = response.text
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Execution Error: {e}")
