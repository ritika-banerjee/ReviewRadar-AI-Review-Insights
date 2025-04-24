from transformers import BartForConditionalGeneration, BartTokenizer
import torch
import re

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def preprocess_df(df):
    """
    Cleans and processes the review text by removing URLs, special characters, and excessive whitespace.
    """
    texts = df["review_text"].dropna().astype(str).tolist()
    
    cleaned_texts = []
    for text in texts:
        text = re.sub(r"http\S+", "", text)  # remove URLs
        text = re.sub(r"[^a-zA-Z0-9.,!?\\s]", "", text)  # remove special chars
        text = re.sub(r"\s+", " ", text)  # normalize whitespace
        cleaned_texts.append(text.strip())

    return cleaned_texts


def summarize_text(df):
    """
    Summarizes all negative reviews in the DataFrame using a pre-trained BART model.
    Outputs the summary as a list of bullet points.
    """
    complaints_df = df[df["sentiment"] == "NEGATIVE"]
    
    if complaints_df.empty:
        print("No negative reviews to summarize.")
        return "No negative reviews to summarize."
    
    # Preprocess all the negative reviews
    reviews = preprocess_df(complaints_df)
    
    # Combine all negative reviews into one string (considering length limits)
    combined_text = " ".join(reviews)
    
    # If the text is too long, we break it into chunks of 1024 tokens
    max_input_length = 1024
    chunks = [combined_text[i:i+max_input_length] for i in range(0, len(combined_text), max_input_length)]
    
    summaries = []
    
    # Summarize each chunk of text
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", max_length=max_input_length, truncation=True, padding="longest")
        summary_ids = model.generate(inputs["input_ids"], max_length=100, min_length=40, num_beams=6, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    
    # Combine all the individual summaries into one final summary
    final_summary = " ".join(summaries)
    
    # Split the summary into points (separated by periods or newlines)
    points = final_summary.split(".")
    points = [point.strip() for point in points if point.strip()]  # Remove empty points
    
    # Format as bullet points
    bullet_points = "\n".join([f"- {point}" for point in points])
    
    return bullet_points


def summarize_reviews(df):
    """
    Summarizes all negative reviews from the DataFrame using the pre-trained BART model.
    Outputs the result as a list of bullet points.
    
    Args:
        df (pd.DataFrame): DataFrame containing reviews with a 'sentiment' column.
    
    Returns:
        str: Final summary of all negative reviews in bullet points.
    """
    summary = summarize_text(df)
    
    return summary
