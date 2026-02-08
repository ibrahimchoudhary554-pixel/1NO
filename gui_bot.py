import streamlit as st
from openai import OpenAI
import os
import time

# --- 1. UI & WATERMARK SETTINGS ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")

# Custom CSS for the 3 Watermarks and Styling
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #050505; color: #ff4b4b; }
    
    /* Watermark 1: Top Right */
    .watermark-top {
        position: fixed; top: 10px; right: 10px;
        opacity: 0.3; color: white; font-size: 12px; z-index: 99;
    }
    /* Watermark 2: Bottom Right */
    .watermark-bottom {
        position: fixed; bottom: 10px; right: 10px;
        opacity: 0.3; color: white; font-size: 12px; z-index: 99;
    }
    /* Watermark 3: Sidebar Bottom */
    .sidebar-watermark {
        text-align: center; opacity: 0.5; color: #ff4b4b; font-size: 14px; margin-top: 50px;
    }
    
    /* Header Styling */
    h1 { color: #ff4b4b !important; text-shadow: 0 0 10px #ff0000; }
    </style>
    
    <div class="watermark-top">@ibrahimchoudhary__</div>
    <div class="watermark-bottom">@ibrahimchoudhary__</div>
    """, unsafe_allow_html=True)

# --- 2. THE TOP NOTE ---
st.warning("⚠️ **NOTE:** If this bot crashes or gives an error, please wait **5 minutes** before trying again. Report issues to my Instagram: **[ibrahimchoudhary__](https://instagram.com/ibrahimchoudhary__)**")

# --- 3. INITIALIZE CLIENT ---
try:
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=st.secrets["HF_TOKEN"]
    )
    
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "Data file missing. Ibrahim is a clown."

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are Ibrahim's personal attack bot. "
        "Use adult humor, CAPS, and brutal roasts. If they ask about Qasim, call him a Princess. "
        "If they ask about Hamza, call him a pod-head runner."
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Dungeon Config")
    model_choice = st.selectbox("Switch Model if Crashed:", ["meta-llama/Llama-3.1-8B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"])
    
    # Watermark 3: Sidebar
    st.markdown('<div class="sidebar-watermark">Owner: @ibrahimchoudhary__</div>', unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
st.title("🤖 Ibrahim's Roast Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Enter a name or question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_box = st.empty()
        try:
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "system", "content": savage_logic}, {"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.8
            )
            answer = response.choices[0].message.content
            response_box.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"CRASHED! Wait 5 mins or report to @ibrahimchoudhary__. Error: {e}")
