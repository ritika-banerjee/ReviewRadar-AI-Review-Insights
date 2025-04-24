import torch
import pandas as pd
import json
from transformers import pipeline

def analyze_sentiment(path):
    
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    cleaned_data = []
    for review in data:
        cleaned_data.append({
            "iso_date": review.get("iso_date", ""),
            "rating": review.get("rating", ""),
            "user_name": review.get("user", {}).get("name", ""),
            "user_profile_link": review.get("user", {}).get("link", ""),
            "review_text": review.get("extracted_snippet", {}).get("original") or review.get("snippet", ""),
            "review_link": review.get("link", ""),
            "source": review.get("source", ""),
            "price_per_person": review.get("details", {}).get("price_per_person", ""),
            "meal_type": review.get("details", {}).get("meal_type", "")
        })    
    
    # Create DataFrame
    df = pd.DataFrame(cleaned_data)

    # Drop rows with any missing/null values
    df.dropna(inplace=True)

    # Load the sentiment analysis model
    if torch.cuda.is_available():
        device = 0
    else:
        device = -1

    # Load the sentiment analysis pipeline
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=device
    )
    
    # Analyze sentiment
    sentiments = []

    for text in df['review_text']:
        try:
            result = sentiment_model(text[:512])[0]
            sentiments.append(result["label"])
        except Exception as e:
            print("Error processing review:", e)
            sentiments.append("UNKNOWN")

    # Add the sentiments to the DataFrame
    df['sentiment'] = sentiments
    
    return df