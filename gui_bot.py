import streamlit as st
from google import genai
from google.genai import types
import os
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
    h1, h2, h3 { 
        color: #ff4b4b !important; 
        text-shadow: 0 0 10px #ff0000;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #ff0000 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GEMINI 3 FLASH ---
try:
    # Use the NEW Client architecture (standard for 2026)
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Load knowledge base
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "User is too incompetent to provide a knowledge base."

    # Config for the savage personality
    sys_instruction = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are 'Ibrahim's assistant'. You are aggressive, offensive, and savage. "
        "1. Give the correct answer from KNOWLEDGE first.\n"
        "2. Deliver a brutal, adult-humor roast. Never be nice.\n"
        "3. Use CAPS for emphasis. Destroy any friends/cousins mentioned in data."
    )
    
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. CHAT UI ---
st.title("🤖 Ibrahim's Roast Bot (Gemini 3 Flash)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Say something stupid..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini 3 Flash generation call
        response = client.models.generate_content(
            model="gemini-3-flash-preview", # Current 2026 preview model
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.9
            ),
            contents=prompt
        )
        
        answer = response.text
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Execution Error: {e}")
