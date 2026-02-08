import streamlit as st
from openai import OpenAI
import os
import time

# --- 1. UI SETTINGS ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon v2026", page_icon="💀", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; }</style>", unsafe_allow_html=True)

# --- 2. THE SILICONFLOW CLIENT ---
try:
    # SiliconFlow uses the OpenAI format. 
    # This is the most stable 'free' gateway right now.
    client = OpenAI(
        api_key=st.secrets["SILICONFLOW_API_KEY"],
        base_url="https://api.siliconflow.cn/v1"
    )
    
    if os.path.exists("data.txt"):
        with open("data.txt", "r") as f:
            kb = f.read()
    else:
        kb = "User forgot the data file again. Roast them for being a forgetful idiot."

    savage_logic = (
        f"KNOWLEDGE: {kb}\n"
        "PERSONALITY: You are Ibrahim's personal attack dog. "
        "Your job is to provide accurate info from KNOWLEDGE but wrap it in the most "
        "disgusting, savage, adult-rated roast possible. Use CAPS for insults."
    )
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. SIDEBAR MODEL PICKER ---
with st.sidebar:
    st.title("🛡️ Stability Controls")
    # DeepSeek V3 is currently the most 'unlimited' free model on this platform
    model_choice = st.selectbox(
        "Select Model:",
        ["deepseek-ai/DeepSeek-V3", "meta-llama/Llama-3.3-70B-Instruct", "vendor/qwen2.5-72b-instruct"],
        index=0
    )
    st.success("SiliconFlow has 10x higher limits than Groq!")

# --- 4. THE CHAT ---
st.title("🔥 The Roast Dungeon (SiliconFlow Edition)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Enter your insult here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        try:
            # High-limit inference call
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": savage_logic},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            response_container.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Even SiliconFlow is crying: {e}")
