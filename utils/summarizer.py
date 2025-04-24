import pandas as pd
import torch
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration
import streamlit as st
import time

@st.cache_resource
def load_models():
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    tokenizer = T5Tokenizer.from_pretrained("t5-small") 
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    return embedder, tokenizer, model

embedder, summ_tokenizer, summ_model = load_models()

def preprocess_text(texts):
    cleaned = []
    for t in texts:
        t = t.replace("\n", " ").replace("\\", "").strip()
        cleaned.append(t[:300])  
    return cleaned

def cluster_reviews(df, num_clusters=3):
    texts = preprocess_text(df["review_text"].dropna().astype(str).tolist())

    embeddings = embedder.encode(texts, convert_to_tensor=True)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings.cpu().numpy())

    clusters = {}
    for label, review in zip(labels, texts):
        clusters.setdefault(label, []).append(review)

    return clusters

def summarize_cluster(texts):

    texts = texts[:5]  
    input_text = " ".join(texts)

    prompt = f"Summarize the following customer reviews and give key insights:\n{input_text}"
    inputs = summ_tokenizer(prompt, return_tensors="pt", truncation=True)
    
    summary_ids = summ_model.generate(inputs.input_ids, max_length=100, min_length=40, num_beams=4)
    summary = summ_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def cluster_based_summary(df, num_clusters=2):
    clusters = cluster_reviews(df, num_clusters=num_clusters)
    final_summary = ""

    for cluster_id, reviews in clusters.items():
        summary = summarize_cluster(reviews)
        final_summary += f"\n**Cluster {cluster_id + 1} Summary:**\n{summary}\n\n"

    return final_summary.strip()

def summarize_reviews_cluster(df, num_clusters=3):
    return cluster_based_summary(df, num_clusters=num_clusters)
