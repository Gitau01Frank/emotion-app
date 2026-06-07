import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.api import send_message, check_colab_status

EMOTION_EMOJI = {
    "joy"    : "😊",
    "sadness": "😢",
    "anger"  : "😠",
    "fear"   : "😨",
    "disgust": "🤢",
    "shame"  : "😳",
    "guilt"  : "😔",
    "unknown": "❓"
}

EMOTION_COLOR = {
    "joy"    : "#FFD700",
    "sadness": "#4169E1",
    "anger"  : "#FF4500",
    "fear"   : "#800080",
    "disgust": "#228B22",
    "shame"  : "#FF8C00",
    "guilt"  : "#808080",
    "unknown": "#CCCCCC"
}

def show_chat():
    st.title("💬 Emotion-Aware Support Chat")
    st.markdown(
        "Share how you are feeling and receive "
        "a compassionate response."
    )

    # Colab status
    status_r = check_colab_status()

    if status_r and status_r.status_code == 200:
        status = status_r.json()
        if status["colab_connected"]:
            st.success("🟢 DistilBERT connected via Colab GPU")
        else:
            st.error("🔴 Colab not connected.")
            st.info(
                "**To connect:**\n"
                "1. Open Colab notebook\n"
                "2. Enable GPU\n"
                "3. Run all cells\n"
                "4. Copy ngrok URL to .env as COLAB_API_URL\n"
                "5. Restart FastAPI backend"
            )
            return
    else:
        st.error("🔴 Cannot reach backend. Is FastAPI running?")
        st.code("cd backend\nuvicorn main:app --reload --port 8000")
        return

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    # Display messages
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user_message"])

        with st.chat_message("assistant"):
            emotion = chat["emotion"]
            emoji   = EMOTION_EMOJI.get(emotion, "💬")
            color   = EMOTION_COLOR.get(emotion, "#CCCCCC")

            st.markdown(
                f"<span style='background-color:{color};"
                f"padding:4px 12px;border-radius:12px;"
                f"color:white;font-weight:bold;font-size:13px'>"
                f"{emoji} {emotion.upper()}</span>"
                f"&nbsp;&nbsp;"
                f"<span style='color:gray;font-size:12px'>"
                f"{chat['confidence']}% confidence</span>",
                unsafe_allow_html=True
            )
            st.write("")
            st.write(chat["gpt_response"])

            with st.expander("📊 See all emotion probabilities"):
                prob_df = pd.DataFrame(
                    list(chat["all_probs"].items()),
                    columns=["Emotion", "Probability (%)"]
                ).sort_values("Probability (%)", ascending=False)
                st.dataframe(prob_df, use_container_width=True)

    # Input
    user_input = st.chat_input("How are you feeling today?")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Analysing your emotion..."):
            try:
                response = send_message(user_input)

                if response.status_code == 200:
                    data    = response.json()
                    emotion = data.get("emotion", "unknown")
                    emoji   = EMOTION_EMOJI.get(emotion, "💬")
                    color   = EMOTION_COLOR.get(emotion, "#CCCCCC")

                    with st.chat_message("assistant"):
                        st.markdown(
                            f"<span style='background-color:{color};"
                            f"padding:4px 12px;border-radius:12px;"
                            f"color:white;font-weight:bold;"
                            f"font-size:13px'>"
                            f"{emoji} {emotion.upper()}</span>"
                            f"&nbsp;&nbsp;"
                            f"<span style='color:gray;font-size:12px'>"
                            f"{data['confidence']}% confidence</span>",
                            unsafe_allow_html=True
                        )
                        st.write("")
                        st.write(data["gpt_response"])

                        with st.expander(
                            "📊 See all emotion probabilities"
                        ):
                            prob_df = pd.DataFrame(
                                list(data["all_probs"].items()),
                                columns=["Emotion", "Probability (%)"]
                            ).sort_values(
                                "Probability (%)", ascending=False
                            )
                            st.dataframe(
                                prob_df, use_container_width=True
                            )

                    st.session_state.chat_history.append({
                        "user_message": user_input,
                        "emotion"     : emotion,
                        "confidence"  : data["confidence"],
                        "all_probs"   : data["all_probs"],
                        "gpt_response": data["gpt_response"]
                    })

                else:
                    st.error("Something went wrong. Try again.")

            except Exception as e:
                st.error(f"Error: {str(e)}")