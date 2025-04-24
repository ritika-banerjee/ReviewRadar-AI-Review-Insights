# 📊 ReviewRadar - AI Review Insights

**ReviewRadar** is an AI-powered tool that fetches Google reviews for a business, analyzes them using NLP models, and presents actionable insights through sentiment trends, visualizations, and key complaint summaries. It’s built using **Streamlit**, and leverages state-of-the-art NLP models for summarization and sentiment analysis.

---

## 🚀 Features

- 🔍 **Fetch Reviews**: Automatically pulls reviews for any business on Google.
- 📈 **Sentiment Analysis**: Uses NLP to detect positive, negative, and neutral sentiments.
- 🧠 **AI-Powered Summarization**: Generates a human-readable summary of reviews using cluster-based summarization.
- 📊 **Data Visualizations**: Interactive charts like pie plots, line graphs, heatmaps.
- 📝 **Top Complaints**: Displays the longest and most critical reviews.
- 🗂️ **Local Caching**: Saves reviews, sentiment, and complaint data locally for reanalysis.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Backend**: Python
- **NLP**: Transformers , `scikit-learn`
- **Data**: `Pandas`, `Matplotlib`, `Seaborn`
- **Google Reviews**: Fetched using SerpAPI

---

## 📁 Folder Structure

```
📦ReviewRadar
 ┣ 📂utils
 ┃ ┣ 📜fetch_reviews.py
 ┃ ┣ 📜sentiment.py
 ┃ ┣ 📜summarizer.py
 ┃ ┣ 📜visualize.py
 ┃ ┗ 📜create_folders.py
 ┣ 📜app.py
 ┣ 📜requirements.txt
 ┗ 📜README.md
```

---

## ⚙️ How to Run

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/ReviewRadar.git
   cd ReviewRadar
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Streamlit app**:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Example Use Case

- Enter: `"Karims"` and `"Bhubaneswar"`
- Get:
  - Number of positive/negative reviews
  - Trends over time
  - Key complaints summarized with actionable suggestions

---

## 📦 Dependencies

- `streamlit`
- `pandas`
- `matplotlib`
- `seaborn`
- `textblob`
- `transformers`
- `scikit-learn`
- `nltk`
- `serpapi`

---

## 📌 Todo / Future Improvements

- [ ] Add support for multi-language reviews
- [ ] Deploy as a web app using Streamlit Sharing or HuggingFace Spaces
- [ ] Allow export of summary and charts to PDF
- [ ] Integrate LLM-based feedback generation

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Streamlit](https://streamlit.io/)
