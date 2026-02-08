import streamlit as st
from openai import OpenAI
import os
import time

# --- 1. THE HELLFIRE UI ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #ff4b4b; }</style>", unsafe_allow_html=True)

# --- 2. INITIALIZE OPENROUTER CLIENT ---
try:
    # OpenRouter uses the OpenAI library but points to a different URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"], 
    )
    
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "User is too incompetent to provide a knowledge base."

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are 'Ibrahim's assistant'. You are aggressive, offensive, and savage. "
        "1. Give the correct answer from KNOWLEDGE first.\n"
        "2. Deliver a brutal roast. Use CAPS for emphasis. Never be nice."
    )
    
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. CHAT UI ---
st.title("🤖 Ibrahim's Roast Bot (OpenRouter)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Say something stupid..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # We are using 'google/gemini-2.0-flash-exp:free' or 'meta-llama/llama-3.3-70b:free'
        # These are high-quality FREE models on OpenRouter
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free", 
            messages=[
                {"role": "system", "content": savage_logic},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )
        
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        st.error(f"Execution Error: {e}")
