import random
from datetime import datetime

class ContentGenerator:
    """Service for generating LinkedIn content based on trends [BE-06]"""
    
    def __init__(self):
        """Initialize the ContentGenerator."""
        self.templates = {
            'question': [
                "What do you think about the trending topic of {topic}? #Trending",
                "Have you heard about {topic}? How is it impacting your industry? #Insights",
                "Is {topic} relevant to your business? Let's discuss! #TrendingNow",
                "How could {topic} change the way we work? Share your thoughts! #FutureOfWork"
            ],
            'insight': [
                "Latest trend alert: {topic} is gaining momentum. Here's why it matters... #TrendAnalysis",
                "{topic} is trending today. Here's what you need to know about it... #StayInformed",
                "Trend spotlight: {topic} - Here's what the data shows... #DataInsights",
                "My analysis on why {topic} is trending and what it means for professionals... #ProfessionalDevelopment"
            ],
            'tips': [
                "5 ways {topic} can boost your professional growth... #CareerTips",
                "How to leverage the {topic} trend in your business strategy... #BusinessStrategy",
                "3 things every professional should know about {topic}... #ProfessionalAdvice",
                "Quick guide: Incorporating {topic} into your workflow... #Productivity"
            ],
            'news': [
                "Breaking: {topic} is trending. Here's the latest development... #TrendingNews",
                "Just in: {topic} is making waves in the industry. Read more... #IndustryUpdate",
                "Today's top trend: {topic} - What you need to know... #TrendWatch",
                "Trend report: {topic} is shaping discussions today... #CurrentEvents"
            ]
        }
        
        self.hashtag_templates = [
            "#Trending #LinkedIn #ProfessionalDevelopment",
            "#BusinessTrends #{normalized_topic} #Industry",
            "#{normalized_topic} #TrendAlert #ProfessionalGrowth",
            "#CareerAdvice #TrendingNow #{normalized_topic}"
        ]
        
    def generate_post_ideas(self, trend_data, count=3):
        """
        Generate LinkedIn post ideas based on trend data.
        
        Args:
            trend_data (dict): Trend data with topic information
            count (int): Number of post ideas to generate
            
        Returns:
            list: List of post ideas
        """
        if not trend_data or 'topic' not in trend_data:
            return []
            
        topic = trend_data['topic']
        normalized_topic = self._normalize_topic(topic)
        
        # Generate different types of posts
        post_ideas = []
        post_types = list(self.templates.keys())
        
        for _ in range(count):
            # Choose a random post type
            post_type = random.choice(post_types)
            
            # Get template and fill it
            template = random.choice(self.templates[post_type])
            post_content = template.format(topic=topic)
            
            # Add hashtags
            hashtag_template = random.choice(self.hashtag_templates)
            hashtags = hashtag_template.format(normalized_topic=normalized_topic)
            
            # Create the post idea
            post_idea = {
                'content': post_content,
                'hashtags': hashtags,
                'full_post': f"{post_content}\n\n{hashtags}",
                'type': post_type,
                'topic': topic,
                'generated_at': datetime.now().isoformat()
            }
            
            post_ideas.append(post_idea)
            
        return post_ideas
    
    def generate_content_from_trends(self, trends_list, count_per_trend=1):
        """
        Generate content ideas from a list of trends.
        
        Args:
            trends_list (list): List of trend data objects
            count_per_trend (int): Number of content ideas per trend
            
        Returns:
            list: List of content ideas
        """
        all_ideas = []
        
        for trend in trends_list:
            ideas = self.generate_post_ideas(trend, count=count_per_trend)
            all_ideas.extend(ideas)
            
        return all_ideas
    
    def _normalize_topic(self, topic):
        """Convert a topic to a hashtag-friendly format."""
        # Remove special characters and spaces
        normalized = ''.join(c for c in topic if c.isalnum() or c.isspace())
        
        # Convert to camel case
        words = normalized.split()
        if not words:
            return ''
            
        return ''.join([words[0].lower()] + [w.capitalize() for w in words[1:]])
    
    def enrich_post_with_analytics(self, post_idea, trend_analytics):
        """
        Enrich a post idea with trend analytics data.
        
        Args:
            post_idea (dict): Post idea
            trend_analytics (dict): Analytics data for the trend
            
        Returns:
            dict: Enriched post idea
        """
        if not trend_analytics:
            return post_idea
            
        # Create a copy of the post idea
        enriched_post = post_idea.copy()
        
        # Add analytics data
        enriched_post['analytics'] = {
            'interest_level': trend_analytics.get('current_interest', 0),
            'rising_trend': trend_analytics.get('rising', False),
            'best_time_to_post': self._suggest_posting_time(),
            'estimated_engagement': self._estimate_engagement(trend_analytics)
        }
        
        return enriched_post
    
    def _suggest_posting_time(self):
        """Suggest the best time to post on LinkedIn."""
        # These are general best practices for LinkedIn
        best_times = [
            "Tuesday 8:00-10:00 AM",
            "Wednesday 8:00-10:00 AM",
            "Thursday 9:00-11:00 AM",
            "Tuesday 5:00-6:00 PM",
            "Wednesday 3:00-5:00 PM"
        ]
        
        return random.choice(best_times)
    
    def _estimate_engagement(self, trend_analytics):
        """Estimate potential engagement based on trend analytics."""
        interest_level = trend_analytics.get('current_interest', 0)
        rising = trend_analytics.get('rising', False)
        
        # Simple heuristic for engagement estimation
        if rising and interest_level > 75:
            return "High"
        elif rising or interest_level > 50:
            return "Medium"
        else:
            return "Low" 