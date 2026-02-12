import streamlit as st
from openai import OpenAI

# --- 1. UI & DARK MODE STYLING ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.5; color: white; font-size: 12px; }
    .header-text { text-align: center; color: #ff4b4b; font-size: 40px; font-weight: bold; }
    </style>
    <div class="header-text">🔥 THE ROAST DUNGEON 🔥</div>
    <div class="watermark">Created by Ibrahim</div>
    """, unsafe_allow_html=True)

# --- 2. CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous roasts
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 3. THE ROAST LOGIC ---
if prompt := st.chat_input("Enter a name to destroy..."):
    # Show user's input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # The "Safe List" - Ibrahim is untouchable
        is_safe = any(n in prompt.lower() for n in ["ibrahim", "owner", "zainab"])
        
        if is_safe:
            system_msg = "You are a humble, loyal servant. Be extremely polite and protective."
        else:
            system_msg = "You are a savage, brutal roast bot. Use hilarious adult humor. Be mean and funny."

        try:
            # Connect to Hugging Face
            client = OpenAI(
                base_url="https://router.huggingface.co/v1", 
                api_key=st.secrets["HF_TOKEN"]
            )
            
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct", # Using this because it's the fastest right now
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9 # High temperature = more creative roasts
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error("Rate limit hit! Hugging Face is tired. Wait 60 seconds.")
