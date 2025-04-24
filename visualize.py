import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/mnt/mydrive/Reelo/data_with_sentiment.csv')

df['iso_date'] = pd.to_datetime(df['iso_date'])
df['date'] = df['iso_date'].dt.date

sentiment_trend = df.groupby(["date", "sentiment"]).size().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
sentiment_trend.plot(kind='line', marker='o', ax=plt.gca())

plt.title("Sentiment Trend Over Time (Karim's Reviews)")
plt.xlabel("Date")
plt.ylabel("Number of Reviews")
plt.grid(True)
plt.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("sentiment_trend.png")

sentiment_counts = df["sentiment"].value_counts()

labels = sentiment_counts.index
sizes = sentiment_counts.values
colors = ['#66bb6a', '#ef5350']  # Green for positive, red for negative

# Plot the pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops={'edgecolor': 'black'}
)
plt.title("Sentiment Distribution (Positive vs Negative Reviews)")
plt.axis('equal')  # Equal aspect ratio for a perfect circle
plt.tight_layout()

# Save the pie chart
plt.savefig("sentiment_pie_chart.png")