import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.api import (get_emotion_counts, get_emotion_trend,
                        get_recent_messages)

def show_dashboard():
    st.title("📊 Emotion Trends Dashboard")
    st.markdown("Insights from all emotion detections over time.")

    # Auto refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()

    # Fetch data
    counts_r   = get_emotion_counts()
    trend_r    = get_emotion_trend()
    messages_r = get_recent_messages()

    if not counts_r or counts_r.status_code != 200:
        st.error("Cannot fetch data. Is the backend running?")
        return

    counts   = counts_r.json()
    trend    = trend_r.json()
    messages = messages_r.json()

    if not counts:
        st.info(
            "No data yet. Go to Chat and send some messages "
            "to see trends here."
        )
        return

    # Summary metrics
    total = sum(counts.values())
    top   = max(counts, key=counts.get)

    col1, col2, col3 = st.columns(3)
    col1.metric("💬 Total Messages",     total)
    col2.metric("🏆 Most Common Emotion", top.upper())
    col3.metric("🎭 Unique Emotions",    len(counts))

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Emotion Distribution")
        counts_df = pd.DataFrame(
            list(counts.items()),
            columns=["Emotion", "Count"]
        )
        fig_pie = px.pie(
            counts_df,
            names  = "Emotion",
            values = "Count",
            color_discrete_sequence = px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition='inside',
                               textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Emotion Counts")
        fig_bar = px.bar(
            counts_df.sort_values("Count", ascending=False),
            x      = "Emotion",
            y      = "Count",
            color  = "Emotion",
            color_discrete_sequence = px.colors.qualitative.Set2,
            text   = "Count"
        )
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # Trend over time
    if trend:
        st.subheader("Emotion Trend Over Time")
        trend_df     = pd.DataFrame(trend)
        trend_counts = trend_df.groupby(
            ['date', 'emotion']
        ).size().reset_index(name='count')

        fig_line = px.line(
            trend_counts,
            x       = "date",
            y       = "count",
            color   = "emotion",
            markers = True,
            color_discrete_sequence = px.colors.qualitative.Set2
        )
        fig_line.update_layout(
            xaxis_title = "Date",
            yaxis_title = "Number of Messages"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    # Recent messages
    if messages:
        st.subheader("Recent Interactions")
        msg_df = pd.DataFrame(messages)[[
            'timestamp', 'text_content',
            'detected_emotion', 'gpt_response'
        ]]
        msg_df.columns = [
            'Time', 'User Message',
            'Emotion', 'GPT Response'
        ]
        st.dataframe(msg_df, use_container_width=True)