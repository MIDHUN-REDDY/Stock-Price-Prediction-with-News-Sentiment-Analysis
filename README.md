# Stock-Price-Prediction-with-News-Sentiment-Analysis

---

## 🧠 Project Overview

Traditional stock price prediction models rely purely on numerical data, often ignoring the *emotional* impact of news and media.  
This project bridges that gap by integrating **real-time news sentiment** with **technical indicators** to enhance prediction accuracy.

**Key Idea:**  
> “Stock prices are driven not just by numbers, but by emotions and opinions reflected in the news.”

---

## 🎯 Objectives
- Collect historical stock data and recent financial news.
- Perform sentiment analysis on news headlines.
- Combine sentiment scores with historical data.
- Train an ML model to predict future stock price movement.
- Visualize results using interactive graphs.

---

## ⚙️ Tech Stack
| Category | Tools / Libraries |
|-----------|-------------------|
| **Programming Language** | Python |
| **Data Collection** | yfinance, NewsAPI / web scraping |
| **Data Analysis** | Pandas, NumPy |
| **Visualization** | Matplotlib, Plotly, Seaborn |
| **Machine Learning** | Scikit-learn, XGBoost |
| **NLP / Sentiment Analysis** | VADER, TextBlob, NLTK |
| **Frontend (optional)** | Streamlit / Flask (for UI) |

---

## 🧩 System Architecture
1. **Data Collection:**  
   Fetch stock data from Yahoo Finance and news headlines from APIs or scraping.

2. **Preprocessing:**  
   Clean, merge, and align datasets by date.

3. **Sentiment Analysis:**  
   Perform NLP to assign polarity scores (positive, neutral, negative).

4. **Feature Engineering:**  
   Combine numerical indicators with sentiment features.

5. **Model Training:**  
   Train ML models like Linear Regression, Random Forest, or LSTM.

6. **Visualization:**  
   Display predicted vs actual prices with trend graphs.

---
