"""
Stock Price Prediction Module using Random Forest Regressor
"""

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import plotly.graph_objects as go
from config import RANDOM_FOREST_ESTIMATORS, RANDOM_FOREST_RANDOM_STATE, TEST_SIZE


class StockPredictor:
    """
    A class to predict stock prices using Random Forest Regressor
    """
    
    def __init__(self, ticker):
        """
        Initialize the StockPredictor with a ticker symbol
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        """
        self.ticker = ticker.upper()
        self.data = None
        self.model = None
        self.prediction = None
        
    def fetch_data(self, period="1y"):
        """
        Fetch historical stock data from Yahoo Finance
        
        Args:
            period (str): Time period for historical data (default: '1y')
            
        Returns:
            bool: True if data fetched successfully, False otherwise
        """
        try:
            # Create ticker with session for better reliability
            stock = yf.Ticker(self.ticker)
            
            # Try different methods to fetch data
            # Method 1: Using history with period
            self.data = stock.history(period=period)
            
            # If empty, try with download method
            if self.data.empty:
                print(f"Trying alternative method for {self.ticker}...")
                self.data = yf.download(self.ticker, period=period, progress=False)
            
            # Check if we have data
            if self.data.empty or len(self.data) < 30:
                print(f"Insufficient data for {self.ticker}")
                return False
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in self.data.columns for col in required_columns):
                print(f"Missing required columns for {self.ticker}")
                return False
                
            return True
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return False
    
    def prepare_features(self):
        """
        Prepare features for the machine learning model
        
        Returns:
            tuple: (X, y) features and target variable
        """
        df = self.data.copy()
        
        # Create technical indicators as features
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['Volatility'] = df['Close'].rolling(window=10).std()
        df['Price_Change'] = df['Close'].pct_change()
        df['Volume_Change'] = df['Volume'].pct_change()
        
        # Create target variable (next day's closing price)
        df['Target'] = df['Close'].shift(-1)
        
        # Drop NaN values
        df.dropna(inplace=True)
        
        # Select features
        features = ['Open', 'High', 'Low', 'Close', 'Volume', 
                   'MA_5', 'MA_10', 'MA_20', 'Volatility', 
                   'Price_Change', 'Volume_Change']
        
        X = df[features]
        y = df['Target']
        
        return X, y
    
    def train_model(self):
        """
        Train the Random Forest Regressor model
        
        Returns:
            dict: Model performance metrics
        """
        X, y = self.prepare_features()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_FOREST_RANDOM_STATE, shuffle=False
        )
        
        # Initialize and train the model
        self.model = RandomForestRegressor(
            n_estimators=RANDOM_FOREST_ESTIMATORS,
            random_state=RANDOM_FOREST_RANDOM_STATE,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy metrics
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        return {
            'train_score': train_score,
            'test_score': test_score
        }
    
    def predict_next_day(self):
        """
        Predict the next day's closing price
        
        Returns:
            float: Predicted closing price
        """
        # Prepare the latest data point for prediction
        X, _ = self.prepare_features()
        latest_features = X.iloc[-1:]
        
        # Make prediction with feature names to avoid warning
        self.prediction = self.model.predict(latest_features)[0]
        
        return self.prediction
    
    def get_current_price(self):
        """
        Get the most recent closing price
        
        Returns:
            float: Current closing price
        """
        return self.data['Close'].iloc[-1]
    
    def generate_chart(self):
        """
        Generate an interactive price chart using Plotly
        
        Returns:
            str: JSON representation of the Plotly figure
        """
        fig = go.Figure()
        
        # Add closing price trace
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=self.data['Close'],
            mode='lines',
            name='Closing Price',
            line=dict(color='#2E86AB', width=2)
        ))
        
        # Add moving averages
        ma_20 = self.data['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=self.data.index,
            y=ma_20,
            mode='lines',
            name='20-Day MA',
            line=dict(color='#A23B72', width=1, dash='dash')
        ))
        
        # Update layout
        fig.update_layout(
            title=f'{self.ticker} - One Year Stock Price History',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            font=dict(family="Arial, sans-serif", size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig.to_json()
    
    def get_stock_info(self):
        """
        Get additional stock information
        
        Returns:
            dict: Stock information including company name
        """
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return {
                'company_name': info.get('longName', self.ticker),
                'symbol': self.ticker,
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A')
            }
        except:
            return {
                'company_name': self.ticker,
                'symbol': self.ticker,
                'currency': 'USD',
                'exchange': 'N/A'
            }

