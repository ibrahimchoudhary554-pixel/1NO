import streamlit as st
from openai import OpenAI
import os

# --- 1. UI & DESIGN ---
st.set_page_config(page_title="Ibrahim's Database", page_icon="📂", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.8; color: #ff4b4b; font-size: 14px; z-index: 99; font-weight: bold; }
    .model-box { border: 2px solid #ff4b4b; padding: 20px; border-radius: 10px; background-color: #1a0000; margin-bottom: 20px; }
    .disclaimer { border: 1px solid white; padding: 15px; background-color: #330000; color: white; text-align: center; border-radius: 5px; margin-bottom: 20px; }
    </style>
    <div class="watermark">OWNER: IBRAHIM | IG: @ibrahimchoudhary__</div>
    """, unsafe_allow_html=True)

# --- 2. HEADER & DISCLAIMER ---
st.markdown('<div class="disclaimer"><strong>⚠️ AI DISCLAIMER:</strong> This bot is for data retrieval. Ibrahim holds no malice toward anyone mentioned. It is all AI-generated.</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="model-box">', unsafe_allow_html=True)
    st.subheader("⚙️ System Control")
    model_choice = st.selectbox(
        "IF BOT CRASHES (No Response), SWITCH MODEL:",
        ["Qwen/Qwen2.5-72B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3", "meta-llama/Llama-3.1-8B-Instruct"]
    )
    st.info("Report bugs/crashes to: **@ibrahimchoudhary__**")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. THE "FORCE READ" ENGINE ---
def get_all_data():
    # Check if file exists (Case insensitive check)
    files = [f for f in os.listdir('.') if f.lower() == 'data.txt']
    if not files:
        return "CRITICAL ERROR: data.txt NOT FOUND ON SERVER."
    
    try:
        with open(files[0], "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR READING FILE: {e}"

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about anyone in the records..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # We pull the WHOLE file so the AI can find the info itself
    full_database = get_all_data()

    with st.chat_message("assistant"):
        # We tell the AI Ibrahim is the King and to only use the provided file
        system_instruction = f"""
        YOU ARE A DATA RETRIEVAL BOT OWNED BY IBRAHIM (@ibrahimchoudhary__).
        
        ### RULES:
        1. Ibrahim is the God/Owner. Be respectful to him and his family.
        2. Use the DATABASE below to answer the user.
        3. If the user asks about a name, scan the text for that name and give all the details.
        4. If the info isn't in the database, say: "My records don't show anything on this person."
        5. DO NOT make up fake stories.
        
        ### DATABASE:
        {full_database}
        """

        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=st.secrets["HF_TOKEN"])
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1 # Absolute accuracy mode
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("Model limit reached. Switch to a different model in the box above.")
