import streamlit as st
import os
import json
import pandas as pd

from utils.fetch_reviews import fetch_reviews
from utils.summarizer import summarize_reviews_cluster
from utils.visualize import(
    plot_pie, plot_trend,
    plot_rating_by_meal, plot_sentiment_by_price,
    plot_weekday_heatmap, get_longest_negative_reviews
)
from utils.sentiment import analyze_sentiment
from utils.create_folders import create_business_folder


# Streamlit settings
st.set_page_config(
    page_title="ReviewRadar - AI Review Insights",
    page_icon="📊",
    layout="wide",
)

# ---------- HEADER ----------
st.markdown("""
<style>
.big-title {
    font-size: 36px !important;
    font-weight: bold;
    color: #3B3B3B;
}
.subheading {
    font-size: 20px !important;
    color: #5e5e5e;
    margin-top: -10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📊 ReviewRadar</div>', unsafe_allow_html=True)
st.markdown('<div class="subheading">AI-powered Google Review Analyzer for Smart Businesses</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------- FORM ----------
with st.form("review_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input("🏢 Business Name", placeholder="e.g. Karims")
    with col2:
        location = st.text_input("📍 Location", placeholder="e.g. Bhubaneswar")
    submitted = st.form_submit_button("🔍 Analyze")

if submitted:
    folder = create_business_folder(business_name, location)
    reviews_path = os.path.join(folder, "reviews.json")
    sentiment_path = os.path.join(folder, "sentiment.csv")
    complaints_path = os.path.join(folder, "complaints.csv")

    with st.spinner("🔁 Fetching reviews from Google..."):
        reviews = fetch_reviews(business_name, location)
        with open(reviews_path, "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=4)

    with st.spinner("🧠 Analyzing sentiment..."):
        df = analyze_sentiment(reviews_path)
        df.to_csv(sentiment_path, index=False)

    # ---------- KPIs ----------
    st.markdown("### 📌 Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", f"{len(df)}")
    col2.metric("👍 Positive", f"{(df['sentiment'] == 'POSITIVE').sum()}")
    col3.metric("👎 Negative", f"{(df['sentiment'] == 'NEGATIVE').sum()}")

    st.divider()

   # ---------- CHARTS ----------
    st.markdown("### 📊 Sentiment Breakdown")

    # First Row: Pie + Trend
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("🟢 Sentiment Distribution")
        st.pyplot(plot_pie(df), use_container_width=True)
    with chart_col2:
        st.subheader("📈 Sentiment Trend Over Time")
        st.pyplot(plot_trend(df), use_container_width=True)

    st.markdown("---")

    # Second Row: Meal Type + Price Range
    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        st.subheader("🍽️ Average Rating by Meal Type")
        st.pyplot(plot_rating_by_meal(df), use_container_width=True)
    with chart_col4:
        st.subheader("💸 Sentiment by Price Range")
        st.pyplot(plot_sentiment_by_price(df), use_container_width=True)

    st.markdown("---")

    # Third Row: Weekday Heatmap
    st.subheader("🗓️ Review Volume by Weekday")
    st.pyplot(plot_weekday_heatmap(df), use_container_width=True)

    st.divider()
    
    st.markdown("### 🕵️ Top 5 Longest Complaints")
    longest = get_longest_negative_reviews(df)
    for r in longest:
        st.markdown(f"**{r['date']} | {r['user']} | ⭐ {r['rating']}**")
        st.info(r["text"])
    
    # ---------- SUMMARY ----------
    st.markdown("### 🤖 AI Summary")
    with st.spinner("Generating summary..."):
        summary = summarize_reviews_cluster(df, num_clusters=3)
        st.markdown("#### 💡 Key Clustered Insights")
        st.markdown(summary)

