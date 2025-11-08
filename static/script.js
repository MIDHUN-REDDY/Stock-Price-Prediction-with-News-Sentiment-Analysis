/**
 * Stock Price Prediction & News Sentiment Analysis
 * Frontend JavaScript
 */

// Handle Enter key press in input field
document.getElementById('ticker-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        predictStock();
    }
});

/**
 * Main function to predict stock and analyze sentiment
 */
async function predictStock() {
    const tickerInput = document.getElementById('ticker-input');
    const ticker = tickerInput.value.trim().toUpperCase();
    
    // Validation
    if (!ticker) {
        showError('Please enter a stock ticker symbol');
        return;
    }
    
    // Hide previous results and errors
    hideResults();
    hideError();
    
    // Show loading state
    showLoading(true);
    
    try {
        // Make API request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ticker: ticker })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred while fetching data');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server. Please try again.');
    } finally {
        showLoading(false);
    }
}

/**
 * Display all results on the page
 */
function displayResults(data) {
    // Show results section
    document.getElementById('results-section').style.display = 'block';
    
    // Update stock information
    document.getElementById('company-name').textContent = data.company_name;
    document.getElementById('ticker-symbol').textContent = data.ticker;
    document.getElementById('exchange-info').textContent = 
        `${data.exchange} • Currency: ${data.currency}`;
    
    // Update prediction values
    document.getElementById('current-price').textContent = 
        `$${data.current_price.toFixed(2)}`;
    document.getElementById('predicted-price').textContent = 
        `$${data.predicted_price.toFixed(2)}`;
    
    // Update price change with color coding
    const priceChangeElement = document.getElementById('price-change');
    const changeSign = data.price_change >= 0 ? '+' : '';
    priceChangeElement.textContent = 
        `${changeSign}$${data.price_change.toFixed(2)} (${changeSign}${data.price_change_percent.toFixed(2)}%)`;
    priceChangeElement.style.color = data.price_change >= 0 ? '#48bb78' : '#f56565';
    
    // Update model accuracy
    const accuracy = (data.model_accuracy.test_score * 100).toFixed(2);
    document.getElementById('model-accuracy').textContent = `${accuracy}%`;
    
    // Display chart
    displayChart(data.chart_data);
    
    // Display sentiment analysis
    displaySentiment(data.sentiment);
    
    // Scroll to results
    document.getElementById('results-section').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
}

/**
 * Display the stock price chart
 */
function displayChart(chartData) {
    const chartDiv = document.getElementById('stock-chart');
    const figure = JSON.parse(chartData);
    Plotly.newPlot(chartDiv, figure.data, figure.layout, {responsive: true});
}

/**
 * Display sentiment analysis results
 */
function displaySentiment(sentiment) {
    // Update sentiment counts
    document.getElementById('positive-count').textContent = sentiment.positive_count;
    document.getElementById('neutral-count').textContent = sentiment.neutral_count;
    document.getElementById('negative-count').textContent = sentiment.negative_count;
    
    // Update sentiment description
    document.getElementById('sentiment-description').textContent = 
        sentiment.sentiment_description;
    
    // Display news articles
    displayNewsArticles('positive-news', sentiment.positive_articles, 'positive');
    displayNewsArticles('negative-news', sentiment.negative_articles, 'negative');
    displayNewsArticles('neutral-news', sentiment.neutral_articles, 'neutral');
}

/**
 * Display news articles for a specific sentiment category
 */
function displayNewsArticles(elementId, articles, sentiment) {
    const container = document.getElementById(elementId);
    
    if (!articles || articles.length === 0) {
        container.innerHTML = '<p class="no-news">No articles found in this category</p>';
        return;
    }
    
    container.innerHTML = '';
    
    articles.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = `news-item ${sentiment}`;
        
        const title = document.createElement('div');
        title.className = 'news-title';
        title.textContent = article.title || 'No title';
        
        const description = document.createElement('div');
        description.className = 'news-description';
        description.textContent = article.description || 'No description available';
        
        const meta = document.createElement('div');
        meta.className = 'news-meta';
        
        const source = document.createElement('span');
        source.className = 'news-source';
        source.textContent = article.source || 'Unknown Source';
        
        const link = document.createElement('a');
        link.className = 'news-link';
        link.href = article.url;
        link.target = '_blank';
        link.textContent = 'Read More →';
        
        meta.appendChild(source);
        meta.appendChild(link);
        
        articleDiv.appendChild(title);
        articleDiv.appendChild(description);
        articleDiv.appendChild(meta);
        
        container.appendChild(articleDiv);
    });
}

/**
 * Show loading state
 */
function showLoading(loading) {
    const button = document.getElementById('predict-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');
    
    if (loading) {
        button.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        button.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorSection = document.getElementById('error-section');
    const errorMessage = document.getElementById('error-message');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Scroll to error
    errorSection.scrollIntoView({ 
        behavior: 'smooth',
        block: 'center'
    });
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('error-section').style.display = 'none';
}

/**
 * Hide results section
 */
function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

/**
 * Format date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

