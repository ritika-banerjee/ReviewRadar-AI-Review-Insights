import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


def plot_pie(df):
    sentiment_counts = df["sentiment"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#66bb6a', '#ef5350']
    )
    ax.set_title("Sentiment Distribution")
    ax.axis('equal')
    return fig


def plot_trend(df):
    df["iso_date"] = pd.to_datetime(df["iso_date"])
    df["date"] = df["iso_date"].dt.date

    trend = df.groupby(["date", "sentiment"]).size().unstack().fillna(0)

    fig, ax = plt.subplots()
    trend.plot(ax=ax, marker="o")
    ax.set_title("Sentiment Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_rating_by_meal(df):
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="meal_type", y="rating", errorbar=None, palette="Blues_d", ax=ax)
    ax.set_title("Average Rating per Meal Type")
    ax.set_ylabel("Avg Rating")
    ax.set_xlabel("Meal Type")
    plt.tight_layout()
    return fig


def plot_sentiment_by_price(df):
    fig, ax = plt.subplots()
    sns.countplot(data=df, x="price_per_person", hue="sentiment", palette="Set2", ax=ax)
    ax.set_title("Sentiment Distribution by Price Range")
    ax.set_xlabel("Price per Person")
    ax.set_ylabel("Number of Reviews")
    plt.tight_layout()
    return fig


def plot_weekday_heatmap(df):
    df["iso_date"] = pd.to_datetime(df["iso_date"])
    df["weekday"] = df["iso_date"].dt.day_name()

    weekday_counts = df["weekday"].value_counts().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])

    fig, ax = plt.subplots()
    sns.heatmap(weekday_counts.to_frame().T, annot=True, fmt=".1f", cmap="YlOrRd", cbar=False, ax=ax)
    ax.set_title("Review Volume by Weekday")
    ax.set_yticks([])
    plt.tight_layout()
    return fig


def get_longest_negative_reviews(df, top_n=5):
    negatives = df[df["sentiment"] == "NEGATIVE"]
    longest = negatives.sort_values(by="review_text", key=lambda x: x.str.len(), ascending=False).head(top_n)
    
    review_list = []
    for idx, row in longest.iterrows():
        review_list.append({
            "date": row["iso_date"],
            "user": row["user_name"],
            "rating": row["rating"],
            "text": row["review_text"][:300] + "..."
        })
    return review_list
