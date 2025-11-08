"""
News Sentiment Analysis Module using VADER and News API
"""

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
from config import NEWS_API_KEY, NEWS_API_URL


class SentimentAnalyzer:
    """
    A class to fetch news and perform sentiment analysis
    """
    
    def __init__(self, ticker, company_name=None):
        """
        Initialize the SentimentAnalyzer
        
        Args:
            ticker (str): Stock ticker symbol
            company_name (str): Company name for better search results
        """
        self.ticker = ticker
        self.company_name = company_name if company_name else ticker
        self.analyzer = SentimentIntensityAnalyzer()
        self.news_articles = []
        
    def fetch_news(self, days_back=7, max_articles=50):
        """
        Fetch news articles from News API
        
        Args:
            days_back (int): Number of days to look back for news
            max_articles (int): Maximum number of articles to fetch
            
        Returns:
            bool: True if news fetched successfully, False otherwise
        """
        try:
            # Calculate date range
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days_back)
            
            # Prepare API request
            params = {
                'q': f'{self.company_name} OR {self.ticker}',
                'from': from_date.strftime('%Y-%m-%d'),
                'to': to_date.strftime('%Y-%m-%d'),
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': max_articles,
                'apiKey': NEWS_API_KEY
            }
            
            # Make API request
            response = requests.get(NEWS_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'ok':
                self.news_articles = data.get('articles', [])
                return True
            else:
                print(f"News API error: {data.get('message', 'Unknown error')}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return False
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of a given text using VADER
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment scores and classification
        """
        scores = self.analyzer.polarity_scores(text)
        
        # Classify sentiment based on compound score
        if scores['compound'] >= 0.05:
            sentiment = 'positive'
        elif scores['compound'] <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment': sentiment
        }
    
    def analyze_all_news(self):
        """
        Analyze sentiment for all fetched news articles
        
        Returns:
            dict: Comprehensive sentiment analysis results
        """
        positive_articles = []
        negative_articles = []
        neutral_articles = []
        
        for article in self.news_articles:
            # Combine title and description for analysis
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}"
            
            # Skip if no meaningful text
            if not text.strip() or text.strip() == '.':
                continue
            
            # Analyze sentiment
            sentiment_result = self.analyze_sentiment(text)
            
            # Create article summary
            article_summary = {
                'title': title,
                'description': description,
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published_at': article.get('publishedAt', ''),
                'sentiment_score': sentiment_result['compound'],
                'sentiment': sentiment_result['sentiment']
            }
            
            # Categorize by sentiment
            if sentiment_result['sentiment'] == 'positive':
                positive_articles.append(article_summary)
            elif sentiment_result['sentiment'] == 'negative':
                negative_articles.append(article_summary)
            else:
                neutral_articles.append(article_summary)
        
        # Calculate overall sentiment
        total_articles = len(positive_articles) + len(negative_articles) + len(neutral_articles)
        
        if total_articles == 0:
            overall_sentiment = 'neutral'
            sentiment_description = 'No news articles found for analysis'
        else:
            positive_ratio = len(positive_articles) / total_articles
            negative_ratio = len(negative_articles) / total_articles
            
            if positive_ratio > 0.5:
                overall_sentiment = 'positive'
                sentiment_description = f'Predominantly positive news coverage ({positive_ratio*100:.1f}% positive)'
            elif negative_ratio > 0.5:
                overall_sentiment = 'negative'
                sentiment_description = f'Predominantly negative news coverage ({negative_ratio*100:.1f}% negative)'
            elif positive_ratio > negative_ratio:
                overall_sentiment = 'slightly_positive'
                sentiment_description = f'Mixed with slight positive bias ({positive_ratio*100:.1f}% positive, {negative_ratio*100:.1f}% negative)'
            elif negative_ratio > positive_ratio:
                overall_sentiment = 'slightly_negative'
                sentiment_description = f'Mixed with slight negative bias ({negative_ratio*100:.1f}% negative, {positive_ratio*100:.1f}% positive)'
            else:
                overall_sentiment = 'neutral'
                sentiment_description = f'Balanced news coverage ({positive_ratio*100:.1f}% positive, {negative_ratio*100:.1f}% negative)'
        
        return {
            'total_articles': total_articles,
            'positive_count': len(positive_articles),
            'negative_count': len(negative_articles),
            'neutral_count': len(neutral_articles),
            'positive_articles': positive_articles[:5],  # Top 5
            'negative_articles': negative_articles[:5],  # Top 5
            'neutral_articles': neutral_articles[:5],    # Top 5
            'overall_sentiment': overall_sentiment,
            'sentiment_description': sentiment_description
        }

