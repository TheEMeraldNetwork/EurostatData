from flask import Blueprint, jsonify, request
from services.trends_service import TrendsService
from services.content_generator import ContentGenerator

# Create blueprint
content_bp = Blueprint('content', __name__)

# Initialize services
trends_service = TrendsService()
content_generator = ContentGenerator()

@content_bp.route('/suggestions', methods=['POST'])
def generate_content_suggestions():
    """Generate content suggestions based on trend data."""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Request body is required'
            }), 400
            
        # Get parameters
        topic = data.get('topic')
        region = data.get('region', '')
        count = int(data.get('count', 3))
        
        # Validate parameters
        if not topic:
            return jsonify({
                'status': 'error',
                'message': 'Topic parameter is required'
            }), 400
            
        # Limit count to a reasonable number
        if count > 10:
            count = 10
            
        # Get trend data for the topic
        trend_data = {
            'topic': topic,
            'details': {}
        }
        
        # Try to enrich with real trend data if available
        try:
            search_results = trends_service.search_trends(
                keywords=[topic],
                geo=region
            )
            
            if search_results.get('interest_over_time'):
                # Extract analytics data
                interest_data = search_results['interest_over_time']
                if interest_data:
                    current_interest = interest_data[-1].get(topic, 0)
                    trend_data['details'] = {
                        'current_interest': current_interest,
                        'rising': current_interest > 50  # Arbitrary threshold
                    }
        except Exception as e:
            # Continue with basic trend data if analytics fails
            print(f"Error enriching trend data: {e}")
            
        # Generate content suggestions
        suggestions = content_generator.generate_post_ideas(trend_data, count=count)
        
        # Enrich suggestions with analytics if available
        enriched_suggestions = []
        for suggestion in suggestions:
            enriched_suggestion = content_generator.enrich_post_with_analytics(
                suggestion,
                trend_data['details']
            )
            enriched_suggestions.append(enriched_suggestion)
            
        return jsonify({
            'status': 'success',
            'data': enriched_suggestions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@content_bp.route('/suggestions/bulk', methods=['POST'])
def generate_bulk_content_suggestions():
    """Generate content suggestions for multiple trends."""
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Request body is required'
            }), 400
            
        # Get parameters
        topics = data.get('topics', [])
        region = data.get('region', '')
        count_per_topic = int(data.get('count_per_topic', 1))
        
        # Validate parameters
        if not topics:
            return jsonify({
                'status': 'error',
                'message': 'Topics parameter is required'
            }), 400
            
        # Limit count to a reasonable number
        if count_per_topic > 5:
            count_per_topic = 5
            
        # Limit number of topics to process
        topics = topics[:10]
        
        # Process each topic
        all_suggestions = []
        
        for topic in topics:
            # Create trend data
            trend_data = {
                'topic': topic,
                'details': {}
            }
            
            # Generate suggestions
            suggestions = content_generator.generate_post_ideas(trend_data, count=count_per_topic)
            all_suggestions.extend(suggestions)
            
        return jsonify({
            'status': 'success',
            'data': all_suggestions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@content_bp.route('/suggestions/trending', methods=['GET'])
def generate_trending_content_suggestions():
    """Generate content suggestions based on current trending topics."""
    try:
        # Get query parameters
        region = request.args.get('region', '')
        count = int(request.args.get('count', 5))
        count_per_trend = int(request.args.get('count_per_trend', 1))
        
        # Limit count to a reasonable number
        if count > 10:
            count = 10
            
        if count_per_trend > 3:
            count_per_trend = 3
            
        # Get current trending topics
        trends = trends_service.get_current_trends(geo=region)
        
        # Limit to requested number of trends
        trends = trends[:count]
        
        # Generate content suggestions for each trend
        all_suggestions = content_generator.generate_content_from_trends(
            trends,
            count_per_trend=count_per_trend
        )
            
        return jsonify({
            'status': 'success',
            'data': all_suggestions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 