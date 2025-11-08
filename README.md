# 📈 Stock Price Prediction & News Sentiment Analysis

A full-stack web application that predicts stock prices using machine learning and analyzes news sentiment to provide comprehensive insights for investors.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-orange.svg)
![License](https://img.shields.io/badge/License-Educational-red.svg)

## 🌟 Features

### Stock Price Prediction
- **Historical Data Analysis**: Fetches one year of stock price data from Yahoo Finance
- **Machine Learning Model**: Uses Random Forest Regressor to predict next-day closing prices
- **Technical Indicators**: Incorporates moving averages, volatility, and price changes
- **Interactive Charts**: Beautiful, responsive price charts using Plotly
- **Model Accuracy**: Displays training and testing accuracy metrics

### News Sentiment Analysis
- **Real-time News**: Fetches latest financial news using News API
- **NLP Sentiment Analysis**: Uses VADER sentiment analysis for accurate classification
- **Sentiment Categories**: Classifies news as Positive, Negative, or Neutral
- **Article Summaries**: Displays top headlines with links to full articles
- **Overall Sentiment**: Provides comprehensive sentiment overview

### User Interface
- **Modern Design**: Professional, gradient-based UI with smooth animations
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Updates**: Dynamic loading states and error handling
- **Interactive Elements**: Hover effects, smooth scrolling, and intuitive navigation

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Web framework for API endpoints
- **scikit-learn**: Machine learning library for Random Forest model
- **yfinance**: Yahoo Finance API for stock data
- **Plotly**: Interactive data visualization
- **VADER Sentiment**: Natural language processing for sentiment analysis
- **pandas & numpy**: Data manipulation and analysis

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Dynamic client-side functionality
- **Plotly.js**: Interactive chart rendering

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for fetching stock data and news)
- News API key (already configured in the project)

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
cd "C:\Users\seeth\OneDrive\Desktop\ml project"
```

### Step 2: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- yfinance (Stock data)
- pandas (Data manipulation)
- numpy (Numerical computing)
- scikit-learn (Machine learning)
- plotly (Data visualization)
- vaderSentiment (Sentiment analysis)
- requests (HTTP library)
- flask-cors (CORS support)

### Step 3: Verify Installation

Check if all packages are installed correctly:

```bash
pip list
```

### Step 4: Run the Application

Start the Flask server:

```bash
python app.py
```

You should see:

```
╔════════════════════════════════════════════════════════════╗
║  Stock Price Prediction & News Sentiment Analysis         ║
║  Server starting on http://localhost:5000                  ║
╚════════════════════════════════════════════════════════════╝
```

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

## 📱 How to Use

1. **Enter Stock Ticker**: Type a valid stock ticker symbol (e.g., AAPL, TSLA, MSFT, GOOGL)
2. **Click Predict**: Press the "Predict" button or hit Enter
3. **View Results**: 
   - See the predicted next-day price
   - Analyze the one-year price chart
   - Review sentiment analysis of recent news
4. **Explore News**: Click on "Read More" links to view full articles

## 📊 Example Stock Tickers

Try these popular stocks:

- **AAPL** - Apple Inc.
- **TSLA** - Tesla Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **AMZN** - Amazon.com Inc.
- **META** - Meta Platforms Inc. (Facebook)
- **NVDA** - NVIDIA Corporation
- **NFLX** - Netflix Inc.

## 🏗️ Project Structure

```
ml-project/
│
├── app.py                      # Main Flask application
├── stock_predictor.py          # Stock prediction module
├── sentiment_analyzer.py       # Sentiment analysis module
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── templates/
│   └── index.html             # Main HTML page
│
└── static/
    ├── style.css              # CSS styling
    └── script.js              # JavaScript functionality
```

## 🔧 Configuration

The `config.py` file contains all configurable settings:

```python
NEWS_API_KEY = "your_api_key_here"  # News API key
HISTORICAL_DAYS = 365               # Days of historical data
RANDOM_FOREST_ESTIMATORS = 100      # Number of trees in forest
TEST_SIZE = 0.2                     # Train/test split ratio
PORT = 5000                         # Server port
```

## 🤖 How It Works

### Stock Prediction Algorithm

1. **Data Collection**: Fetches 1 year of historical stock data
2. **Feature Engineering**: Creates technical indicators:
   - 5, 10, and 20-day moving averages
   - Volatility (10-day standard deviation)
   - Price change percentage
   - Volume change percentage
3. **Model Training**: Trains Random Forest Regressor with 100 decision trees
4. **Prediction**: Uses trained model to predict next day's closing price
5. **Visualization**: Generates interactive chart with Plotly

### Sentiment Analysis Process

1. **News Fetching**: Retrieves recent news articles from News API
2. **Text Processing**: Combines article titles and descriptions
3. **VADER Analysis**: Applies VADER sentiment scoring:
   - Compound score > 0.05: Positive
   - Compound score < -0.05: Negative
   - Otherwise: Neutral
4. **Categorization**: Groups articles by sentiment
5. **Summary Generation**: Creates overall sentiment report

## 📈 API Endpoints

### POST `/api/predict`

Predicts stock price and analyzes news sentiment.

**Request Body:**
```json
{
    "ticker": "AAPL"
}
```

**Response:**
```json
{
    "success": true,
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "current_price": 150.25,
    "predicted_price": 152.30,
    "price_change": 2.05,
    "price_change_percent": 1.36,
    "model_accuracy": {
        "train_score": 0.9876,
        "test_score": 0.9234
    },
    "chart_data": "...",
    "sentiment": {
        "total_articles": 25,
        "positive_count": 15,
        "negative_count": 5,
        "neutral_count": 5,
        "overall_sentiment": "positive",
        "sentiment_description": "Predominantly positive news coverage",
        "positive_articles": [...],
        "negative_articles": [...],
        "neutral_articles": [...]
    }
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "message": "Stock Prediction API is running"
}
```

## ⚠️ Troubleshooting

### Common Issues

**1. Module Not Found Error**
```bash
pip install -r requirements.txt
```

**2. Port Already in Use**
Change the PORT in `config.py` or kill the process:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**3. News API Error**
- Check your internet connection
- Verify API key in `config.py`
- API has rate limits (500 requests/day for free tier)

**4. Invalid Ticker Symbol**
- Ensure the ticker symbol is valid and traded on major exchanges
- Use uppercase (e.g., AAPL, not aapl)

## 📝 Important Notes

### Disclaimer

⚠️ **This application is for educational purposes only and should not be used for actual trading decisions.**

- Stock predictions are based on historical data and may not reflect future performance
- News sentiment is automated and may not capture nuanced market conditions
- Always consult with financial professionals before making investment decisions
- Past performance does not guarantee future results

### Limitations

- Predictions are for next-day closing price only
- Model accuracy varies by stock volatility
- News API has rate limits (500 requests/day for free tier)
- Requires internet connection for real-time data

## 🔐 Security

- API key is stored in `config.py` (do not share publicly)
- No user data is collected or stored
- All requests are processed server-side
- CORS is enabled for local development

## 🎯 Future Enhancements

Potential improvements:
- Multiple day predictions
- Additional ML models (LSTM, Prophet)
- Technical indicators dashboard
- Portfolio tracking
- Email alerts
- Historical sentiment trends
- Comparative stock analysis

## 👨‍💻 Development

### Running in Development Mode

```bash
# Enable debug mode (already enabled in config.py)
python app.py
```

### Testing Individual Modules

```python
# Test stock predictor
from stock_predictor import StockPredictor
predictor = StockPredictor('AAPL')
predictor.fetch_data()
predictor.train_model()
print(predictor.predict_next_day())

# Test sentiment analyzer
from sentiment_analyzer import SentimentAnalyzer
analyzer = SentimentAnalyzer('AAPL', 'Apple Inc.')
analyzer.fetch_news()
results = analyzer.analyze_all_news()
print(results)
```

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure you have a stable internet connection
4. Check console logs for detailed error messages

## 📄 License

This project is created for educational purposes. Feel free to modify and use for learning.

## 🙏 Acknowledgments

- **Yahoo Finance** for stock market data
- **News API** for financial news articles
- **VADER Sentiment** for sentiment analysis
- **Plotly** for interactive visualizations
- **scikit-learn** for machine learning tools

---

**Happy Predicting! 📊📈**

