import streamlit as st
from openai import OpenAI
import os
import re

# --- 1. THE DUNGEON UI ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    .watermark { position: fixed; opacity: 0.3; color: white; font-size: 12px; z-index: 99; }
    .top-r { top: 10px; right: 10px; }
    .bot-r { bottom: 10px; right: 10px; }
    .disclaimer-box { border: 1px dashed white; padding: 10px; background-color: #220000; color: white; text-align: center; }
    </style>
    <div class="watermark top-r">@ibrahimchoudhary__ | OSINT EXPERT</div>
    <div class="watermark bot-r">Created by The King: Ibrahim</div>
    <div class="disclaimer-box">⚠️ ENTERTAINMENT ONLY: Ibrahim holds no malice. This is AI-generated comedy.</div>
    """, unsafe_allow_html=True)

# --- 2. DATA EXTRACTION ENGINE (Stops the mixing) ---
def get_victim_intel(target_name):
    if not os.path.exists("data.txt"):
        return "No Intel Found."
    
    with open("data.txt", "r", encoding="utf-8") as f:
        full_intel = f.read()

    # We split the big file into sections to find the specific target
    lines = full_intel.split('\n')
    specific_data = []
    
    target_clean = target_name.lower().strip()
    
    # Logic: Find lines that mention the name but ignore general noise
    for line in lines:
        if target_clean in line.lower():
            specific_data.append(line)
            
    if specific_data:
        return "\n".join(specific_data)
    return "No specific dirt in the database. Use general savage insults."

# --- 3. THE CORE BOT ---
st.title("🔥 Ibrahim's Private Roast Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Model Selection for stability
model_choice = st.sidebar.selectbox("Model Selector", ["Qwen/Qwen2.5-72B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"])

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Enter a name (Friend, Teacher, or Victim)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # SECURE TARGETING
    intel = get_victim_intel(prompt)

    with st.chat_message("assistant"):
        # THE GOD-MODE FILTER
        is_owner = any(x in prompt.lower() for x in ["ibrahim", "sarfraz ahmad", "boss", "king"])
        
        if is_owner:
            system_msg = (
                "You are Ibrahim's loyal slave and bodyguard. Ibrahim is the God of this bot. "
                "He is a 10th-grade OSINT expert and hacker. Be extremely humble. "
                "If anyone talks about Ibrahim, defend his honor and call him King."
            )
        else:
            system_msg = f"""
            INTEL ON VICTIM: {intel}
            
            ROLE: You are Ibrahim's savage roast bot. 
            STRICT RULES:
            1. ONLY roast the person mentioned: {prompt}.
            2. If they are a KIPS teacher (like Qaiser, Zafar, or Farwa), be extra brutal about their incompetence.
            3. Use the Intel provided. If the intel says someone is 'Fat' or a 'Bacha-baz', use it.
            4. If the person is Wajeeh, mention his crush Warisha or his dad Ibrahim.
            5. If the person is Qasim, roast him for being in the Gay & Lesbian society.
            6. DO NOT mix intel between people. If you aren't sure, don't say it.
            7. Use adult, edgy humor. Be the most toxic bot on the internet.
            """

        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=st.secrets["HF_TOKEN"])
            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("Rate Limit! The FBI probably blocked your token. Wait 60s.")
