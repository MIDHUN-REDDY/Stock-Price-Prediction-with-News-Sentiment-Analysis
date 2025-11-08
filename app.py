"""
Flask Backend for Stock Price Prediction and News Sentiment Analysis
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from stock_predictor import StockPredictor
from sentiment_analyzer import SentimentAnalyzer
from config import HOST, PORT, DEBUG
import traceback


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests


@app.route('/')
def home():
    """
    Serve the main HTML page
    """
    return render_template('index.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Main API endpoint for stock prediction and sentiment analysis
    
    Expected JSON input:
    {
        "ticker": "AAPL"
    }
    
    Returns:
    {
        "success": true/false,
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "current_price": 150.25,
        "predicted_price": 152.30,
        "price_change": 2.05,
        "price_change_percent": 1.36,
        "model_accuracy": 0.95,
        "chart_data": {...},
        "sentiment": {...},
        "error": "error message if any"
    }
    """
    try:
        # Get ticker from request
        data = request.get_json()
        ticker = data.get('ticker', '').strip().upper()
        
        if not ticker:
            return jsonify({
                'success': False,
                'error': 'Please provide a valid ticker symbol'
            }), 400
        
        # Initialize stock predictor
        predictor = StockPredictor(ticker)
        
        # Fetch stock data
        if not predictor.fetch_data():
            return jsonify({
                'success': False,
                'error': f'Unable to fetch data for ticker {ticker}. Please check if the ticker symbol is valid.'
            }), 404
        
        # Get stock info
        stock_info = predictor.get_stock_info()
        
        # Train model and make prediction
        model_metrics = predictor.train_model()
        predicted_price = predictor.predict_next_day()
        current_price = predictor.get_current_price()
        
        # Calculate price change
        price_change = predicted_price - current_price
        price_change_percent = (price_change / current_price) * 100
        
        # Generate chart
        chart_data = predictor.generate_chart()
        
        # Perform sentiment analysis
        sentiment_analyzer = SentimentAnalyzer(ticker, stock_info['company_name'])
        
        sentiment_result = {
            'total_articles': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'positive_articles': [],
            'negative_articles': [],
            'neutral_articles': [],
            'overall_sentiment': 'neutral',
            'sentiment_description': 'Unable to fetch news articles'
        }
        
        if sentiment_analyzer.fetch_news():
            sentiment_result = sentiment_analyzer.analyze_all_news()
        
        # Prepare response
        response = {
            'success': True,
            'ticker': ticker,
            'company_name': stock_info['company_name'],
            'currency': stock_info['currency'],
            'exchange': stock_info['exchange'],
            'current_price': round(current_price, 2),
            'predicted_price': round(predicted_price, 2),
            'price_change': round(price_change, 2),
            'price_change_percent': round(price_change_percent, 2),
            'model_accuracy': {
                'train_score': round(model_metrics['train_score'], 4),
                'test_score': round(model_metrics['test_score'], 4)
            },
            'chart_data': chart_data,
            'sentiment': sentiment_result
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in predict endpoint: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Stock Prediction API is running'
    }), 200


if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║  Stock Price Prediction & News Sentiment Analysis         ║
    ║  Server starting on http://localhost:{PORT}                   ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    app.run(host=HOST, port=PORT, debug=DEBUG)

