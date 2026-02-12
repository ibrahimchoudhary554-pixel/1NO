import streamlit as st
from openai import OpenAI
import os

# --- 1. UI SETTINGS ---
st.set_page_config(page_title="Ibrahim's Roast Dungeon", page_icon="🔥", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ff4b4b; }
    .disclaimer-box { border: 1px dashed white; padding: 10px; background-color: #220000; color: white; text-align: center; }
    </style>
    <div class="disclaimer-box">⚠️ ENTERTAINMENT ONLY: Ibrahim is the King. This is AI humor.</div>
    """, unsafe_allow_html=True)

# --- 2. DATA EXTRACTION ENGINE ---
def get_intel(target_name):
    if not os.path.exists("data.txt"):
        return "The data.txt file is missing from the server."
    
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Split content by sections (using the ### or double newlines in your file)
    sections = content.split('\n\n')
    relevant_context = []
    
    name = target_name.lower().strip()
    
    # Search every section of your data file for the victim's name
    for section in sections:
        if name in section.lower():
            relevant_context.append(section)
            
    if relevant_context:
        # Join the found sections together
        return "\n---\n".join(relevant_context)
    
    return "No specific dirt found in data.txt. Roast them based on general vibes."

# --- 3. THE BOT LOGIC ---
st.title("🤖 Ibrahim's Private Roast Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Who are we destroying today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # SECURE DATA RETRIEVAL
    intel_data = get_intel(prompt)

    with st.chat_message("assistant"):
        # Check if the user is talking to the King himself
        is_king = any(x in prompt.lower() for x in ["ibrahim", "sarfraz", "owner", "boss"])
        
        if is_king:
            system_msg = (
                "You are Ibrahim's loyal bodyguard. Ibrahim is an expert in OSINT and hacking. "
                "Be humble, professional, and protective. NEVER roast the King."
            )
        else:
            system_msg = f"""
            KNOWLEDGE BASE FOR THIS VICTIM:
            {intel_data}
            
            ROLE: 
            You are a savage, brutal roast bot created by Ibrahim. 
            
            INSTRUCTIONS:
            1. Use the KNOWLEDGE BASE above to roast {prompt}. 
            2. If they are a KIPS teacher, use their specific 'Hellhole' nicknames (like Zafar Supari or Bubbly).
            3. If the data says they are a 'Milo addict' or 'smokes pot', hit them with that.
            4. Be extremely mean, funny, and use adult humor. 
            5. If the knowledge base is empty, just roast them for being a nobody.
            """

        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=st.secrets["HF_TOKEN"])
            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-72B-Instruct",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=450
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("Rate limit hit! Hugging Face is overloaded. Wait 60s.")
