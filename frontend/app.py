import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title = "Emotion Support App",
    page_icon  = "💬",
    layout     = "wide"
)

# CSS
st.markdown("""
<style>
    .stMetric {
        background-color : white;
        padding          : 15px;
        border-radius    : 10px;
        box-shadow       : 0 2px 4px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        border-radius : 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/color/96/brain.png",
    width=80
)
st.sidebar.title("Emotion Support")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["💬 Chat", "📊 Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**How it works:**
1. 💬 Type how you feel
2. 🧠 DistilBERT detects emotion
3. 🤖 GPT-4o-mini responds
4. 💾 Data saved automatically
5. 📊 View trends on dashboard
""")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small>Powered by DistilBERT + GPT-4o-mini</small>",
    unsafe_allow_html=True
)

# ── Pages ─────────────────────────────────────────────────────
if page == "💬 Chat":
    from pages.chat import show_chat
    show_chat()

elif page == "📊 Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()