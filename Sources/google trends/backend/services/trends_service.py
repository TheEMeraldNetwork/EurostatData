import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import random
import json

class TrendsService:
    """Service for fetching and processing Google Trends data [BE-02]"""
    
    def __init__(self, hl='en-US', tz=360):
        """
        Initialize the TrendsService.
        
        Args:
            hl (str): Language (default 'en-US')
            tz (int): Timezone offset (default 360)
        """
        try:
            # Try with minimal parameters
            self.pytrends = TrendReq(hl=hl, tz=tz)
            self.api_available = True
        except Exception as e:
            print(f"Warning: Error initializing TrendReq: {e}")
            self.api_available = False
            
        # Create mock data for fallback
        self.mock_trending_topics = [
            {"topic": "Artificial Intelligence", "details": {"current_interest": 85, "rising": True}},
            {"topic": "Renewable Energy", "details": {"current_interest": 72, "rising": True}},
            {"topic": "Cybersecurity", "details": {"current_interest": 68, "rising": False}},
            {"topic": "Blockchain", "details": {"current_interest": 65, "rising": False}},
            {"topic": "Remote Work", "details": {"current_interest": 60, "rising": True}},
            {"topic": "Digital Marketing", "details": {"current_interest": 58, "rising": True}},
            {"topic": "E-commerce", "details": {"current_interest": 55, "rising": False}},
            {"topic": "Virtual Reality", "details": {"current_interest": 50, "rising": True}},
            {"topic": "Cloud Computing", "details": {"current_interest": 48, "rising": False}},
            {"topic": "Data Privacy", "details": {"current_interest": 45, "rising": True}}
        ]
        
    def get_current_trends(self, geo='', category=0):
        """Get current trending topics with fallback to mock data."""
        if not self.api_available:
            print("Using mock trending topics (API not available)")
            return self._get_mock_trending_topics()
            
        try:
            trending_searches_df = self.pytrends.trending_searches(pn=geo if geo else 'united_states')
            
            # Format results
            trending_topics = trending_searches_df[0].tolist()
            
            # Get more details for each trending topic
            results = []
            for topic in trending_topics[:10]:  # Limit to top 10 to avoid API rate limits
                details = self._get_topic_details(topic, geo, category)
                results.append({
                    'topic': topic,
                    'details': details
                })
                
            return results
        except Exception as e:
            print(f"Error fetching current trends: {e}")
            return self._get_mock_trending_topics()
        
    def search_trends(self, keywords, geo='', timeframe='today 3-m', category=0):
        """Search for specific keywords with fallback to mock data."""
        if not self.api_available:
            print("Using mock search results (API not available)")
            return self._get_mock_search_results(keywords)
            
        try:
            # Ensure we don't exceed the maximum of 5 keywords
            keywords = keywords[:5]
            
            # Build the payload
            self.pytrends.build_payload(keywords, cat=category, timeframe=timeframe, geo=geo)
            
            # Get the data
            interest_over_time_df = self.pytrends.interest_over_time()
            related_topics = self.pytrends.related_topics()
            related_queries = self.pytrends.related_queries()
            
            # Process and structure the data
            result = {
                'interest_over_time': self._process_interest_over_time(interest_over_time_df),
                'related_topics': self._process_related_topics(related_topics),
                'related_queries': self._process_related_queries(related_queries)
            }
            
            return result
        except Exception as e:
            print(f"Error searching trends: {e}")
            return self._get_mock_search_results(keywords)
        
    def _get_mock_trending_topics(self):
        """Get mocked trending topics for development."""
        # Randomize a bit to simulate different results
        topics = self.mock_trending_topics.copy()
        random.shuffle(topics)
        return topics
        
    def _get_mock_search_results(self, keywords):
        """Get mocked search results for development."""
        # Generate mock time series data
        dates = []
        today = datetime.now()
        for i in range(90):  # ~3 months of daily data
            date = today - timedelta(days=i)
            dates.append(date.strftime('%Y-%m-%d'))
        
        dates.reverse()  # oldest to newest
        
        # Create interest over time with random values for each keyword
        interest_over_time = []
        for date in dates:
            data_point = {'date': date}
            for keyword in keywords:
                # Start with a base value and add some randomness with an upward trend
                base_value = 30 + (dates.index(date) / len(dates)) * 40
                variation = random.randint(-10, 10)
                data_point[keyword] = int(min(100, max(0, base_value + variation)))
            interest_over_time.append(data_point)
        
        # Create mock related topics and queries
        related_topics = {}
        related_queries = {}
        
        for keyword in keywords:
            topic_variations = [
                {"topic_title": f"{keyword} trends", "value": random.randint(60, 100)},
                {"topic_title": f"{keyword} industry", "value": random.randint(40, 80)},
                {"topic_title": f"{keyword} technology", "value": random.randint(30, 70)},
                {"topic_title": f"{keyword} news", "value": random.randint(20, 60)},
                {"topic_title": f"{keyword} companies", "value": random.randint(10, 50)}
            ]
            
            query_variations = [
                {"query": f"what is {keyword}", "value": random.randint(60, 100)},
                {"query": f"{keyword} tutorial", "value": random.randint(40, 80)},
                {"query": f"best {keyword}", "value": random.randint(30, 70)},
                {"query": f"{keyword} examples", "value": random.randint(20, 60)},
                {"query": f"{keyword} vs", "value": random.randint(10, 50)}
            ]
            
            related_topics[keyword] = {
                "rising": topic_variations[:3],
                "top": topic_variations[2:]
            }
            
            related_queries[keyword] = {
                "rising": query_variations[:3],
                "top": query_variations[2:]
            }
        
        return {
            'interest_over_time': interest_over_time,
            'related_topics': related_topics,
            'related_queries': related_queries
        }
    
    def get_regional_trends(self, region, category=0, resolution='COUNTRY'):
        """Get trends for a specific region with fallback to mock data."""
        if not self.api_available:
            print("Using mock regional trends (API not available)")
            return self._get_mock_regional_trends(region)
            
        try:
            # For Italian regions, we need to map region names to ISO codes
            geo_mapping = {
                'lombardia': 'IT-25',
                'lazio': 'IT-62',
                'toscana': 'IT-52',
                # Add more regions as needed
            }
            
            # Default to Italy if specific region not found
            geo = geo_mapping.get(region.lower(), 'IT')
            
            # Get trending searches for the region/country
            trending_searches = self.get_current_trends(geo=geo, category=category)
            
            # Get geographical distribution of top trending topic
            if trending_searches:
                top_topic = trending_searches[0]['topic']
                self.pytrends.build_payload([top_topic], cat=category, geo=geo)
                geo_data = self.pytrends.interest_by_region(resolution=resolution)
                
                # Process geo data
                processed_geo_data = self._process_geo_data(geo_data)
            else:
                processed_geo_data = {}
                
            return {
                'trending_searches': trending_searches,
                'geo_distribution': processed_geo_data
            }
        except Exception as e:
            print(f"Error fetching regional trends: {e}")
            return self._get_mock_regional_trends(region)
            
    def _get_mock_regional_trends(self, region):
        """Get mocked regional trends for development."""
        # Get mock trending topics
        trending_searches = self._get_mock_trending_topics()
        
        # Create mock geo distribution data
        geo_distribution = {}
        
        # For Italy, create regions
        regions = ["Lombardia", "Lazio", "Toscana", "Piemonte", "Veneto", 
                   "Emilia-Romagna", "Campania", "Sicilia", "Puglia", "Calabria"]
                   
        # Get the top topic from trending searches
        if trending_searches:
            top_topic = trending_searches[0]['topic']
            
            # Create interest values for each region
            for r in regions:
                # Higher interest for the requested region
                if r.lower() == region.lower():
                    interest = random.randint(70, 100)
                else:
                    interest = random.randint(20, 80)
                    
                geo_distribution[r] = {top_topic: interest}
        
        return {
            'trending_searches': trending_searches,
            'geo_distribution': geo_distribution
        }
    
    def _get_topic_details(self, topic, geo='', category=0):
        """Get additional details for a trending topic."""
        try:
            self.pytrends.build_payload([topic], cat=category, timeframe='today 1-m', geo=geo)
            
            # Get interest over time
            interest_over_time_df = self.pytrends.interest_over_time()
            
            # Process the data
            if not interest_over_time_df.empty:
                interest_data = interest_over_time_df[topic].tolist()
                current_interest = interest_data[-1] if interest_data else 0
            else:
                current_interest = 0
                
            return {
                'current_interest': current_interest,
                'rising': current_interest > 50  # Arbitrary threshold
            }
        except Exception as e:
            print(f"Error getting details for topic {topic}: {e}")
            return {
                'current_interest': 0,
                'rising': False
            }
    
    def _process_interest_over_time(self, df):
        """Process interest over time data."""
        if df.empty:
            return []
            
        result = []
        for index, row in df.iterrows():
            date_str = index.strftime('%Y-%m-%d')
            data_point = {'date': date_str}
            
            for column in df.columns:
                if column != 'isPartial':
                    data_point[column] = int(row[column])
                    
            result.append(data_point)
            
        return result
    
    def _process_related_topics(self, related_topics):
        """Process related topics data."""
        result = {}
        
        for keyword, data in related_topics.items():
            result[keyword] = {
                'rising': self._process_dataframe(data.get('rising', pd.DataFrame())),
                'top': self._process_dataframe(data.get('top', pd.DataFrame()))
            }
            
        return result
    
    def _process_related_queries(self, related_queries):
        """Process related queries data."""
        result = {}
        
        for keyword, data in related_queries.items():
            result[keyword] = {
                'rising': self._process_dataframe(data.get('rising', pd.DataFrame())),
                'top': self._process_dataframe(data.get('top', pd.DataFrame()))
            }
            
        return result
    
    def _process_dataframe(self, df):
        """Convert a DataFrame to a list of dictionaries."""
        if df.empty:
            return []
            
        return df.to_dict('records')
    
    def _process_geo_data(self, df):
        """Process geographical interest data."""
        if df.empty:
            return {}
            
        # Convert to dictionary with region as key and interest as value
        result = {}
        for index, row in df.iterrows():
            for column in df.columns:
                region_name = index
                interest_value = int(row[column])
                
                if region_name not in result:
                    result[region_name] = {}
                    
                result[region_name][column] = interest_value
                
        return result 