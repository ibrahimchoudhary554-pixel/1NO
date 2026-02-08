import streamlit as st
from openai import OpenAI
import os
import time

# --- 1. THE HELLFIRE UI ---
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

# --- 2. INITIALIZE OPENROUTER ---
try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=st.secrets["OPENROUTER_API_KEY"],
    )
    
    # Load Knowledge Base
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "User is too incompetent to provide a data.txt file."

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are 'Ibrahim's assistant'. You are aggressive, offensive, and savage. "
        "1. Give the correct answer from KNOWLEDGE first.\n"
        "2. Deliver a brutal roast with hard adult humor. Never be nice.\n"
        "3. Use CAPS for emphasis. If the user is a cousin or friend, destroy them."
    )
    
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. SIDEBAR (THE STABILITY HUB) ---
with st.sidebar:
    st.title("⚙️ Dungeon Settings")
    st.subheader("Stability Controls")
    
    # Model Selection - Use these names exactly
    model_choice = st.selectbox(
        "Choose your Weapon:",
        [
            "google/gemini-2.0-flash-exp:free",
            "meta-llama/llama-3.3-70b:free",
            "mistralai/mistral-small-3.1-24b-instruct:free",
            "deepseek/deepseek-r1-distill-qwen-32b:free"
        ],
        index=0,
        help="If one model is overloaded, switch to another free one!"
    )
    
    st.markdown("---")
    st.warning("⚠️ **PRO TIP:** If the bot stops responding on multiple devices, switch the model above to Llama or Mistral.")

# --- 4. CHAT UI ---
st.title("🤖 Ibrahim's Roast Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# User Input
if prompt := st.chat_input("Say something stupid..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logic with Retry & Model Switching
    answer = None
    retries = 3
    
    with st.chat_message("assistant"):
        status_box = st.empty()
        
        for i in range(retries):
            try:
                # OpenRouter API Call
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": savage_logic},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.9
                )
                answer = response.choices[0].message.content
                break # Exit loop if successful
                
            except Exception as e:
                err_msg = str(e).lower()
                if "503" in err_msg or "overloaded" in err_msg:
                    status_box.markdown(f"⏳ *Server overloaded. Retrying ({i+1}/{retries})...*")
                    time.sleep(2)
                else:
                    st.error(f"System Failure: {e}")
                    break
        
        if answer:
            status_box.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            status_box.markdown("❌ **SERVER NUKED.** Switch the model in the sidebar and try again.")
