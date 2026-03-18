import streamlit as st
import requests
import random
import uuid

import os
API_URL = os.getenv("API_URL", "http://fastapi:8000/query")
RESET_URL = os.getenv("RESET_URL", "http://fastapi:8000/reset")

st.set_page_config(
    page_title="AlimBot - Islamic Guidance AI",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if 'selected_qs' not in st.session_state:
    example_questions = [
        "What breaks wudu?",
        "Can I pray with shoes on?",
        "Is fasting on Mondays Sunnah?",
        "What are the rights of parents?",
        "Who can receive zakat?",
        "How to perform Tayammum?",
        "What is the ruling on investing in stocks?",
        "Can women lead prayers?",
        "What are the conditions for a valid marriage in Islam?",
        "Is it permissible to eat food prepared by non-Muslims?",
        "What are the etiquettes of visiting the mosque?",
        "How to calculate prayer times?",
        "What is the significance of Laylat al-Qadr?",
        "Can I delay my prayers for work?",
        "What are the rules for wearing hijab?"
    ]
    st.session_state.selected_qs = random.sample(example_questions, 5)

# --- Custom CSS for Modern Design ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
}

.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(135deg, #008080 0%, #004d4d 100%);
    color: white;
    border-radius: 15px;
    margin-bottom: 2rem;
}

.main-header h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: 600;
}

.main-header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

.stChatMessage {
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}

.example-btn {
    width: 100%;
    margin-bottom: 0.5rem;
    text-align: left !important;
}

</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/mosque.png", width=80)
    st.title("AlimBot Settings")

    st.subheader("💡 Suggested Questions")
    for q in st.session_state.selected_qs:
        if st.button(q, key=f"side_{q}", use_container_width=True):
            st.session_state.query_input = q
            # We don't rerun here to allow user to edit or see what they clicked
            # But actually for better UX, let's just trigger the search if they click an example
            st.session_state.trigger_search = True

    st.divider()

    if st.button("🗑️ Clear Chat History", type="primary", use_container_width=True):
        try:
            requests.post(RESET_URL, json={"session_id": st.session_state.session_id})
            st.session_state.chat_history = []
            st.session_state.query_input = ""
            st.success("History cleared!")
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()
    with st.expander("📘 About AlimBot"):
        st.markdown("""
        **AlimBot** uses advanced AI to provide Islamic guidance based on:
        - 📖 **Quran**
        - 📜 **Hadith**
        - 📚 **Fatwas**

        *Note: AI responses are for informational purposes. Consult scholars for religious rulings.*
        """)

# --- Main Interface ---
st.markdown("""
<div class='main-header'>
    <h1>🕌 AlimBot</h1>
    <p>Your Intelligent Islamic Guidance System</p>
</div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle triggered search from sidebar
if st.session_state.get("trigger_search"):
    query = st.session_state.query_input
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Islamic sources..."):
            try:
                res = requests.post(API_URL, json={
                    "query": query,
                    "session_id": st.session_state.session_id
                })
                if res.status_code == 200:
                    answer = res.json()['result']
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"❌ {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"🚫 Connection error: {e}")

    st.session_state.trigger_search = False
    st.session_state.query_input = ""

# Chat input
if query := st.chat_input("Ask about an Islamic topic..."):
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Islamic sources..."):
            try:
                res = requests.post(API_URL, json={
                    "query": query,
                    "session_id": st.session_state.session_id
                })
                if res.status_code == 200:
                    answer = res.json()['result']
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"❌ {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"🚫 Connection error: {e}")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>🤲 May Allah guide us all with knowledge & wisdom.</div>", unsafe_allow_html=True)
