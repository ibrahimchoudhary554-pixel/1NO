import streamlit as st
from openai import OpenAI
import os

# --- 1. UI & WATERMARK SETTINGS ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    .watermark { position: fixed; opacity: 0.4; color: white; font-size: 14px; z-index: 99; }
    .top-r { top: 10px; right: 10px; }
    .bot-r { bottom: 10px; right: 10px; }
    .model-box { border: 2px solid #ff0000; padding: 15px; border-radius: 10px; background-color: #1a0000; margin-bottom: 20px; }
    .disclaimer-box { border: 1px dashed #ffffff; padding: 10px; background-color: #330000; color: #ffffff; text-align: center; margin-bottom: 15px; }
    </style>
    <div class="watermark top-r">@ibrahimchoudhary__</div>
    <div class="watermark bot-r">@ibrahimchoudhary__</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="disclaimer-box"><strong>⚠️ ENTERTAINMENT ONLY:</strong> Just jokes! Ibrahim has no malice.</div>', unsafe_allow_html=True)

# --- 2. CONFIG ---
SAFE_NAMES = ["ibrahim", "owner", "king", "boss", "zainab"]

# --- 3. HELPER FUNCTION: DATA SEARCH ---
def get_specific_data(name_to_find):
    if not os.path.exists("data.txt"):
        return "No database found."
    
    with open("data.txt", "r") as f:
        lines = f.readlines()
        
    # Search for lines that contain the name
    relevant_info = [line.strip() for line in lines if name_to_find.lower() in line.lower()]
    
    if relevant_info:
        return "\n".join(relevant_info)
    return "No specific dirt found on this person. Roast them generally."

# --- 4. UI ---
st.title("🤖 Ibrahim's Roast Bot")

with st.container():
    st.markdown('<div class="model-box">', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "SWITCH MODEL IF BOT ACTS UP:",
        ["Qwen/Qwen2.5-72B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Enter a name..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search for "dirt" in data.txt
    target_data = get_specific_data(prompt)

    with st.chat_message("assistant"):
        is_safe = any(name in prompt.lower() for name in SAFE_NAMES)
        
        if is_safe:
            system_instruction = (
                "You are Ibrahim's loyal bodyguard. Ibrahim is a VIP. "
                "Be extremely polite, humble, and helpful. DO NOT ROAST. "
                "Speak like a professional royal assistant."
            )
        else:
            system_instruction = (
                f"FACTS ABOUT THE VICTIM: {target_data}\n\n"
                "ROLE: You are Ibrahim's brutal roast bot. "
                "1. If 'FACTS' contains info, use it to destroy them specifically. "
                "2. If no facts exist, roast them based on the name alone. "
                "3. Use hilarious adult humor. Be savage. "
                "4. DO NOT mix data from different people."
            )

        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=st.secrets["HF_TOKEN"])
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7 # Lowered to prevent mixing things up
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"System Overload. Wait 60s. @ibrahimchoudhary__")
