from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta
import time
import random

def download_google_trends_data(keywords, timeframe='today 3-m', geo='IT', max_retries=3):
    """
    Download Google Trends data for specified keywords with retry mechanism
    
    Args:
        keywords (list): List of keywords to search for
        timeframe (str): Time period for the search (default: last 3 months)
        geo (str): Geographic location (default: Italy)
        max_retries (int): Maximum number of retry attempts
    
    Returns:
        dict: Dictionary containing the trends data
    """
    # Initialize pytrends
    pytrends = TrendReq(hl='it-IT', tz=360)
    
    # Initialize empty results
    results = {
        'interest_over_time': None,
        'related_queries': {},
        'related_topics': {}
    }
    
    # Try to get interest over time data with retries
    for attempt in range(max_retries):
        try:
            # Build payload
            pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
            
            # Get interest over time
            interest_over_time_df = pytrends.interest_over_time()
            if interest_over_time_df is not None and not interest_over_time_df.empty:
                results['interest_over_time'] = interest_over_time_df
                break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(5, 10)  # Random wait between 5-10 seconds
                print(f"Waiting {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Max retries reached for interest over time data")
    
    # Get related queries and topics for each keyword
    for keyword in keywords:
        results['related_queries'][keyword] = {'top': None, 'rising': None}
        results['related_topics'][keyword] = {'top': None, 'rising': None}
        
        # Try to get related queries with retries
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(2, 4))  # Random wait between 2-4 seconds
                queries = pytrends.related_queries()
                if keyword in queries and queries[keyword] is not None:
                    results['related_queries'][keyword] = queries[keyword]
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {keyword} queries: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(5, 10)
                    print(f"Waiting {wait_time:.2f} seconds before retrying...")
                    time.sleep(wait_time)
        
        # Try to get related topics with retries
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(2, 4))  # Random wait between 2-4 seconds
                topics = pytrends.related_topics()
                if keyword in topics and topics[keyword] is not None:
                    results['related_topics'][keyword] = topics[keyword]
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {keyword} topics: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(5, 10)
                    print(f"Waiting {wait_time:.2f} seconds before retrying...")
                    time.sleep(wait_time)
    
    return results

def save_data_to_csv(data, prefix='google_trends'):
    """
    Save the downloaded data to CSV files
    
    Args:
        data (dict): Dictionary containing the trends data
        prefix (str): Prefix for the output files
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save interest over time data
    if data['interest_over_time'] is not None and not data['interest_over_time'].empty:
        data['interest_over_time'].to_csv(f'{prefix}_interest_{timestamp}.csv')
        print(f"Saved interest over time data to {prefix}_interest_{timestamp}.csv")
    
    # Save related queries
    for keyword, queries in data['related_queries'].items():
        if queries['top'] is not None and not queries['top'].empty:
            queries['top'].to_csv(f'{prefix}_top_queries_{keyword}_{timestamp}.csv')
            print(f"Saved top queries for {keyword} to {prefix}_top_queries_{keyword}_{timestamp}.csv")
        if queries['rising'] is not None and not queries['rising'].empty:
            queries['rising'].to_csv(f'{prefix}_rising_queries_{keyword}_{timestamp}.csv')
            print(f"Saved rising queries for {keyword} to {prefix}_rising_queries_{keyword}_{timestamp}.csv")
    
    # Save related topics
    for keyword, topics in data['related_topics'].items():
        if topics['top'] is not None and not topics['top'].empty:
            topics['top'].to_csv(f'{prefix}_top_topics_{keyword}_{timestamp}.csv')
            print(f"Saved top topics for {keyword} to {prefix}_top_topics_{keyword}_{timestamp}.csv")
        if topics['rising'] is not None and not topics['rising'].empty:
            topics['rising'].to_csv(f'{prefix}_rising_topics_{keyword}_{timestamp}.csv')
            print(f"Saved rising topics for {keyword} to {prefix}_rising_topics_{keyword}_{timestamp}.csv")

if __name__ == "__main__":
    # Example usage with more general terms
    keywords = ['assicurazioni', 'assicurazione auto', 'assicurazione casa']
    timeframe = 'today 3-m'  # Last 3 months
    geo = 'IT'  # Italy
    
    print("Downloading Google Trends data...")
    data = download_google_trends_data(keywords, timeframe, geo)
    
    print("\nSaving data to CSV files...")
    save_data_to_csv(data)
    
    print("\nDone! Check the generated CSV files in your current directory.") 