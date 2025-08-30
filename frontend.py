import streamlit as st
import requests

# ---- Page Config ----
st.set_page_config(page_title="AI Agentic Chatbot", page_icon="🤖", layout="wide")

# ---- Custom CSS Styling ----
page_style = """
<style>
/* 🌌 Dark linear gradient background */
.stApp {
    background: linear-gradient(135deg, #1f1c2c, #2c3e50, #0f2027);
    background-attachment: fixed;
    animation: darkPulse 20s infinite alternate ease-in-out;
    color: #f0f0f0 !important;
}

/* Gradient animation */
@keyframes darkPulse {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Global font and text color */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    color: #f0f0f0 !important;
}

/* Title and subheader */
.custom-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff !important;
    text-align: center;
    margin-bottom: 10px;
    text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
    animation: fadeInDown 1s ease-out;
}
.subheader {
    font-size: 1.2rem;
    font-weight: 500;
    color: #dddddd !important;
    text-align: center;
    margin-bottom: 30px;
    animation: fadeInDown 1.2s ease-out;
}

/* Chat bubble */
.chat-bubble {
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    padding: 14px 20px;
    margin: 15px 0;
    max-width: 90%;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.3);
    font-size: 1rem;
    line-height: 1.6;
    color: #f0f0f0;
    animation: fadeInUp 0.8s ease-out;
}

/* Animations */
@keyframes fadeInUp {
    0% {opacity: 0; transform: translateY(20px);}
    100% {opacity: 1; transform: translateY(0);}
}
@keyframes fadeInDown {
    0% {opacity: 0; transform: translateY(-20px);}
    100% {opacity: 1; transform: translateY(0);}
}

/* Text areas and inputs */
textarea, .stTextArea textarea,
input, .stTextInput input {
    background: #2c3e50;
    color: #f0f0f0 !important;
    border: 1px solid #555;
    border-radius: 8px;
    font-size: 1rem;
    padding: 10px;
}

/* Labels and widget text */
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stCheckbox label,
.stTextInput label,
.stNumberInput label,
.stSlider label {
    color: #f0f0f0 !important;
    font-weight: 600;
}

/* Radio options */
.stRadio div[role="radiogroup"] label,
.stRadio div[role="radiogroup"] span {
    color: #f0f0f0 !important;
    font-weight: 600;
}

/* Selected radio option */
.stRadio div[aria-checked="true"] {
    background-color: #394867 !important;
    border-left: 4px solid #ff6f61;
    font-weight: 700;
    border-radius: 8px;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# ---- Title ----
st.markdown("<h1 class='custom-title'>🤖 AI Agentic Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>✨ Create and Interact with AI agents using custom prompts and models.</p>", unsafe_allow_html=True)

# ---- Inputs ----
system_prompt = st.text_area("🛠️ Define your AI Agent as", height=100, placeholder="Think like You are Coder")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

st.markdown("### 🌐 Select Model Provider", unsafe_allow_html=True)
provider =  st.radio("Select Provider:", options=["OpenAI", "Groq"])

model_name = st.selectbox("🧠 Select Model", options=MODEL_NAMES_OPENAI if provider == "OpenAI" else MODEL_NAMES_GROQ)

allow_web_search = st.checkbox("🔍 Allow Web Search")
user_query = st.text_area("💬 Enter your Prompt:", height=160, placeholder="Debug My Code")

API_URL = "https://agentic-ai-chatbot-4-mhig.onrender.com/chat"

# ---- Button ----
if st.button("🚀 Ask Agent!"):
    if user_query.strip():
        with st.spinner("🤖 Thinking..."):
            payload = {
                "model_name": model_name,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [{"role": "user", "content": user_query}],
                "allow_search": allow_web_search
            }

            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data['error'])
                else:
                    st.subheader("🤖 Agent Response")
                    st.markdown(
                        f"<div class='chat-bubble'>{response_data['response']}</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.error("❌ Failed to connect to backend server")
