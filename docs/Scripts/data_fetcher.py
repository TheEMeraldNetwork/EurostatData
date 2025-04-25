import json
import os
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

class DataFetcher:
    """
    A utility class to fetch financial and technology trend data to support 
    LinkedIn content creation for financial services and AI thought leadership.
    """
    
    def __init__(self, config_path="news_config.json"):
        """Initialize with API keys from config file"""
        self.config = self._load_config(config_path)
        self.finnhub_key = self.config.get("FINNHUB_KEY")
        self.newsapi_key = self.config.get("NEWSAPI_KEY")
        
    def _load_config(self, config_path):
        """Load API keys from the configuration file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file {config_path} not found")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def get_stock_performance(self, symbols=None, period="3mo"):
        """
        Fetch stock performance data for financial services and tech companies
        
        Args:
            symbols: List of stock symbols to fetch (defaults to a preset list if None)
            period: Time period for data - '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max'
            
        Returns:
            DataFrame with performance data
        """
        if symbols is None:
            symbols = [
                # Insurance
                "G.MI",  # Assicurazioni Generali
                "AXA.PA",  # AXA
                "ALL",  # Allstate
                "CB",  # Chubb
                # Banking
                "ISP.MI",  # Intesa Sanpaolo
                "UCG.MI",  # UniCredit
                "JPM",  # JP Morgan
                "GS",  # Goldman Sachs
                # Tech/AI
                "MSFT",  # Microsoft
                "GOOGL",  # Alphabet
                "NVDA",  # NVIDIA
                "IBM"  # IBM
            ]
            
        results = {}
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period=period)
                
                if not hist.empty:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    percent_change = ((end_price - start_price) / start_price) * 100
                    
                    results[symbol] = {
                        'name': stock.info.get('shortName', symbol),
                        'start_price': start_price,
                        'current_price': end_price,
                        'percent_change': percent_change,
                        'sector': stock.info.get('sector', 'Unknown')
                    }
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                
        return pd.DataFrame(results).T
    
    def get_ai_companies_performance(self, period="3mo"):
        """Fetch performance data for AI-focused companies"""
        ai_symbols = [
            "NVDA",  # NVIDIA
            "MSFT",  # Microsoft
            "GOOGL",  # Alphabet
            "META",  # Meta
            "AMZN",  # Amazon
            "IBM",   # IBM
            "AAPL",  # Apple
            "CRM",   # Salesforce
            "AMD",   # AMD
            "PLTR"   # Palantir
        ]
        
        return self.get_stock_performance(symbols=ai_symbols, period=period)
    
    def get_fintech_performance(self, period="3mo"):
        """Fetch performance data for fintech companies"""
        fintech_symbols = [
            "SQ",    # Block (Square)
            "PYPL",  # PayPal
            "ADYEY",  # Adyen
            "COIN",  # Coinbase
            "V",     # Visa
            "MA",    # Mastercard
            "FISV",  # Fiserv
            "INTU",  # Intuit
            "AVDX",  # AvidXchange
            "NCNO"   # nCino
        ]
        
        return self.get_stock_performance(symbols=fintech_symbols, period=period)
    
    def get_financial_news(self, query=None, limit=10):
        """
        Fetch relevant financial news using NewsAPI
        
        Args:
            query: Search query (default to finance and AI related terms if None)
            limit: Maximum number of news items to return
            
        Returns:
            List of news articles
        """
        if not self.newsapi_key:
            raise ValueError("NewsAPI key not found in config")
        
        if query is None:
            query = "artificial intelligence financial services OR fintech OR AI banking OR AI insurance"
            
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": limit,
            "apiKey": self.newsapi_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                return data.get("articles", [])
            else:
                print(f"Error from NewsAPI: {data.get('message')}")
                return []
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_company_news(self, symbol, from_date=None, to_date=None):
        """
        Fetch company-specific news from Finnhub
        
        Args:
            symbol: Stock symbol of the company
            from_date: Start date for news (defaults to 30 days ago)
            to_date: End date for news (defaults to today)
            
        Returns:
            List of news items for the company
        """
        if not self.finnhub_key:
            raise ValueError("Finnhub API key not found in config")
        
        if from_date is None:
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        if to_date is None:
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        url = "https://finnhub.io/api/v1/company-news"
        params = {
            "symbol": symbol,
            "from": from_date,
            "to": to_date,
            "token": self.finnhub_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching company news for {symbol}: {e}")
            return []
    
    def get_market_sentiment(self, symbols=None):
        """
        Get market sentiment for specified stocks using Finnhub
        
        Args:
            symbols: List of stock symbols (defaults to a preset list if None)
            
        Returns:
            Dictionary with sentiment data by symbol
        """
        if not self.finnhub_key:
            raise ValueError("Finnhub API key not found in config")
            
        if symbols is None:
            symbols = ["G.MI", "AXA.PA", "MSFT", "GOOGL", "NVDA"]
            
        sentiment_data = {}
        
        for symbol in symbols:
            try:
                url = "https://finnhub.io/api/v1/news-sentiment"
                params = {
                    "symbol": symbol,
                    "token": self.finnhub_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                sentiment_data[symbol] = data
                
                # Respect API rate limits
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching sentiment for {symbol}: {e}")
        
        return sentiment_data
    
    def get_ai_trends_topics(self):
        """
        Compile current AI topics and trends in financial services
        based on news headlines and company performance
        
        Returns:
            Dictionary with trending topics and related data
        """
        # Get relevant news
        ai_finance_news = self.get_financial_news(
            query="artificial intelligence financial services innovation",
            limit=20
        )
        
        # Get AI company performance
        ai_performance = self.get_ai_companies_performance()
        
        # Extract topics from headlines and descriptions
        titles = [article.get('title', '') for article in ai_finance_news]
        descriptions = [article.get('description', '') for article in ai_finance_news]
        
        # Simple trend extraction based on common themes
        # (In a real implementation, this would use NLP for better topic extraction)
        topics = {
            "generative_ai": {
                "relevance": 0,
                "articles": []
            },
            "ai_regulation": {
                "relevance": 0,
                "articles": []
            },
            "financial_ai": {
                "relevance": 0,
                "articles": []
            },
            "ai_ethics": {
                "relevance": 0,
                "articles": []
            },
            "ai_adoption": {
                "relevance": 0,
                "articles": []
            }
        }
        
        # Simple keyword matching to categorize articles
        keywords = {
            "generative_ai": ["generative ai", "gpt", "large language model", "llm", "chatgpt", "bard"],
            "ai_regulation": ["regulation", "compliance", "ai act", "regulatory", "gdpr", "policy"],
            "financial_ai": ["financial", "banking", "insurance", "fintech", "finance", "investment"],
            "ai_ethics": ["ethics", "bias", "fairness", "responsible ai", "transparency"],
            "ai_adoption": ["adoption", "implementation", "digital transformation", "enterprise ai"]
        }
        
        for i, article in enumerate(ai_finance_news):
            title = article.get('title', '').lower()
            desc = article.get('description', '').lower()
            content = title + " " + desc
            
            for topic, terms in keywords.items():
                for term in terms:
                    if term in content:
                        topics[topic]["relevance"] += 1
                        topics[topic]["articles"].append(article)
                        break
        
        # Get top performers from AI companies
        if not ai_performance.empty:
            top_performers = ai_performance.nlargest(3, 'percent_change')
            topics["market_leaders"] = {
                "companies": top_performers.index.tolist(),
                "performance": top_performers['percent_change'].tolist()
            }
        
        return topics

    def generate_insights_for_post(self, post_title, post_topic):
        """
        Generate data-driven insights relevant to a specific LinkedIn post
        
        Args:
            post_title: Title of the planned LinkedIn post
            post_topic: Main topic of the post (e.g., 'ai_ethics', 'risk_assessment')
            
        Returns:
            Dictionary with relevant insights for the post
        """
        insights = {
            "market_data": {},
            "news_trends": [],
            "key_statistics": {},
            "relevant_companies": []
        }
        
        # Map post topics to relevant data sources and keywords
        topic_mapping = {
            "ai_ethics": {
                "news_query": "AI ethics financial services responsible AI transparency bias",
                "relevant_symbols": ["MSFT", "GOOGL", "IBM"],
                "key_metrics": ["AI ethics committees", "bias incidents", "regulatory actions"]
            },
            "risk_assessment": {
                "news_query": "AI risk assessment insurance underwriting financial services",
                "relevant_symbols": ["G.MI", "AXA.PA", "ALL", "CB"],
                "key_metrics": ["risk prediction accuracy", "fraud detection rates", "claim processing time"]
            },
            "digital_transformation": {
                "news_query": "digital transformation AI financial services banking insurance",
                "relevant_symbols": ["MSFT", "GOOGL", "IBM", "ORCL", "CRM"],
                "key_metrics": ["IT spending", "digital adoption rates", "process automation savings"]
            },
            "customer_experience": {
                "news_query": "AI customer experience personalization financial services",
                "relevant_symbols": ["CRM", "ADBE", "AMZN", "AAPL"],
                "key_metrics": ["customer satisfaction scores", "engagement rates", "personalization metrics"]
            },
            "regulatory_compliance": {
                "news_query": "AI regulatory compliance financial services banking insurance",
                "relevant_symbols": ["IBM", "MSFT", "ORCL", "NOW"],
                "key_metrics": ["compliance costs", "violation reductions", "regulatory technology spending"]
            }
        }
        
        # Determine the most relevant mapping based on post title and topic
        selected_mapping = None
        for key, mapping in topic_mapping.items():
            if key in post_topic.lower():
                selected_mapping = mapping
                break
        
        # If no direct match, use a default approach
        if not selected_mapping:
            words = post_title.lower().split()
            for key, mapping in topic_mapping.items():
                for word in key.split('_'):
                    if word in words:
                        selected_mapping = mapping
                        break
                if selected_mapping:
                    break
        
        # Use default if still no match
        if not selected_mapping:
            selected_mapping = {
                "news_query": post_title,
                "relevant_symbols": ["MSFT", "GOOGL", "G.MI", "AXA.PA"],
                "key_metrics": ["ROI", "adoption rates", "market growth"]
            }
        
        # Get market data for relevant companies
        market_data = self.get_stock_performance(
            symbols=selected_mapping["relevant_symbols"]
        )
        if not market_data.empty:
            insights["market_data"] = market_data.to_dict(orient="index")
            
            # Extract relevant companies based on performance
            if len(market_data) > 0:
                top_performers = market_data.nlargest(2, 'percent_change')
                insights["relevant_companies"] = [
                    {"symbol": idx, "name": row.get('name', idx), "change": row.get('percent_change')}
                    for idx, row in top_performers.iterrows()
                ]
        
        # Get news trends
        news = self.get_financial_news(
            query=selected_mapping["news_query"],
            limit=5
        )
        
        if news:
            insights["news_trends"] = [
                {
                    "title": item.get("title"),
                    "source": item.get("source", {}).get("name"),
                    "url": item.get("url"),
                    "published_at": item.get("publishedAt")
                }
                for item in news
            ]
        
        # Generate some placeholder statistics relevant to the topic
        # In a real implementation, these would come from actual research or databases
        insights["key_statistics"] = {
            "metric_examples": selected_mapping["key_metrics"],
            "estimated_market_size": "$25-30 billion (Annual AI spending in financial services)",
            "growth_rate": "22% YoY growth in AI adoption in financial sector",
            "success_metric": "35% average cost reduction through AI process automation"
        }
        
        return insights


if __name__ == "__main__":
    # Example usage
    fetcher = DataFetcher()
    
    print("===== AI Companies Performance =====")
    ai_performance = fetcher.get_ai_companies_performance()
    print(ai_performance)
    
    print("\n===== Financial News =====")
    news = fetcher.get_financial_news(limit=3)
    for item in news:
        print(f"Title: {item.get('title')}")
        print(f"Source: {item.get('source', {}).get('name')}")
        print(f"URL: {item.get('url')}")
        print()
    
    print("\n===== Post-Specific Insights =====")
    insights = fetcher.generate_insights_for_post(
        "AI in Risk Assessment: The Next Frontier",
        "risk_assessment"
    )
    print(json.dumps(insights, indent=2)) 