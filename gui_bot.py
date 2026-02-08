import streamlit as st
from openai import OpenAI
import os
import time

# --- 1. THE HELLFIRE UI ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon v3", page_icon="💀", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    section[data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 2px solid #ff0000; }
    h1, h2 { color: #ff4b4b !important; text-shadow: 0 0 8px #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE HUGGING FACE CLIENT ---
try:
    # We use the official Hugging Face OpenAI-compatible router
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=st.secrets["HF_TOKEN"]
    )
    
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "No data.txt found. User is a failure."

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are Ibrahim's savage assistant. "
        "Answer questions from KNOWLEDGE but roast the user brutally using adult humor. "
        "Use CAPS and don't be a snowflake."
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Dungeon Config")
    # Using Llama 3.1 8B because it's the most stable free model on HF right now
    model_choice = st.selectbox(
        "Select Model:",
        [
            "meta-llama/Llama-3.1-8B-Instruct", 
            "mistralai/Mistral-7B-Instruct-v0.3",
            "microsoft/Phi-3-mini-4k-instruct"
        ],
        index=0
    )
    st.info("Hugging Face is currently the most stable free provider.")

# --- 4. CHAT INTERFACE ---
st.title("🔥 Ibrahim's Roast Bot (v2026)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask something, if you dare..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_box = st.empty()
        try:
            # We append ':hf-inference' to force Hugging Face's own servers
            # This bypasses 3rd party provider errors
            full_model_name = f"{model_choice}"
            
            response = client.chat.completions.create(
                model=full_model_name,
                messages=[
                    {"role": "system", "content": savage_logic},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            answer = response.choices[0].message.content
            response_box.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"System Overload: {e}")
            st.warning("Wait 10 seconds. Hugging Face is free, so don't cry about a small delay.")
