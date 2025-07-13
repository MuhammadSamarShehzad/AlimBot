import streamlit as st
import requests
import random

# API_URL = "http://fastapi:8000/query"
API_URL = "https://fastapi-backend.onrender.com/query"

st.set_page_config(page_title="Islamic Guidance AI", page_icon="🕌", layout="centered")

# --- Custom CSS for Modern Design ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

body {
    background: #fafafa;
    font-family: 'Roboto', sans-serif;
}

h1 {
    text-align: center;
    font-size: 2.8rem;
    color: #008080;
    margin-bottom: 0.2rem;
}

.subtext {
    text-align: center;
    color: #555;
    margin-bottom: 2rem;
    font-size: 1.05rem;
}

.input-block, .answer-box {
    background: #fff;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.04);
    margin-bottom: 2rem;
}

.stTextArea textarea {
    font-size: 16px !important;
    padding: 16px;
    border-radius: 10px !important;
    border: 1px solid #ccc;
}

.stButton button {
    background-color: #ff7f50;
    color: white;
    font-size: 16px;
    padding: 10px 28px;
    border-radius: 8px;
    transition: 0.3s ease;
}

.stButton button:hover {
    background-color: #1e1e1e;
    transform: scale(1.02);
}

.answer-box {
    font-size: 1rem;
    line-height: 1.7;
    color: #222;
    border-left: 4px solid #008080;
    padding-left: 16px;
}

hr {
    margin: 3rem 0 1.5rem 0;
    border: none;
    border-top: 1px solid #eee;
}

.footer {
    text-align: center;
    color: #aaa;
    font-size: 12px;
}

/* Ensure example question buttons have uniform size */
.input-block button {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding: 10px 15px;
    background-color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# --- List of Example Questions (Pool of 15) ---
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

# --- Select 5 random questions for this session ---
if 'selected_qs' not in st.session_state:
    st.session_state.selected_qs = random.sample(example_questions, 5)

# --- Header with Banner (Placeholder) ---
# st.image("path_to_banner_image.jpg", use_column_width=True)  # Uncomment and replace with actual image path
st.markdown("<h1>🕌 Islamic Guidance Agent</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Ask your Islamic question and receive a scholarly response powered by Quran, Hadith, and Fatwa.</div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("<div class='input-block'>", unsafe_allow_html=True)

st.subheader("💡 Example Questions")
# Display selected example questions as buttons in columns
cols = st.columns(5)
for col, q in zip(cols, st.session_state.selected_qs):
    if col.button(q, key=q):
        st.session_state.query_input = q

# Text area for user question, pre-filled if an example is selected
query = st.text_area("✍️ Your Question", value=st.session_state.get("query_input", ""), height=140, placeholder="Type or select a question...")

if st.button("👳‍♂️ Ask Now"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("🧠 Thinking..."):
            try:
                res = requests.post(API_URL, json={"query": query})
                if res.status_code == 200:
                    st.markdown(f"<div class='answer-box'><h3>📖 Answer</h3>{res.json()['result']}</div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"🚫 Connection error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Info Section in Expander ---
with st.expander("📘 About This App"):
    st.markdown("""
    This AI assistant provides Islamic rulings with references from:

    - 📖 **Quran**
    - 📜 **Hadith**
    - 📚 **Fatwas**

    Answers structured, citation-based, and locally processed.

    > ⚠️ Always consult a qualified scholar before making decisions based on AI answers.
    """)

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer'>🤲 May Allah guide us all with knowledge & wisdom.</div>", unsafe_allow_html=True)