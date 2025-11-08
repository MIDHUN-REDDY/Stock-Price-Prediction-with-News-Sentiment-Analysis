"""
Configuration file for the Stock Prediction and Sentiment Analysis application
"""

# News API Configuration
NEWS_API_KEY = "0b30e5c69dcc4fd7b4cb33e962f1c8dc"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Stock Data Configuration
HISTORICAL_DAYS = 365  # One year of data
PREDICTION_DAYS = 1    # Predict next day

# Model Configuration
RANDOM_FOREST_ESTIMATORS = 100
RANDOM_FOREST_RANDOM_STATE = 42
TEST_SIZE = 0.2

# Flask Configuration
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

