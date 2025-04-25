from flask import Blueprint, jsonify, request
from services.trends_service import TrendsService

# Create blueprint
trends_bp = Blueprint('trends', __name__)

# Initialize services
trends_service = TrendsService()

@trends_bp.route('/current', methods=['GET'])
def get_current_trends():
    """Get current trending topics."""
    try:
        # Get query parameters
        geo = request.args.get('geo', '')
        category = int(request.args.get('category', 0))
        
        # Get trending topics
        trends = trends_service.get_current_trends(geo=geo, category=category)
        
        return jsonify({
            'status': 'success',
            'data': trends
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@trends_bp.route('/search', methods=['GET'])
def search_trends():
    """Search for specific keywords in Google Trends."""
    try:
        # Get query parameters
        keywords = request.args.get('keywords', '').split(',')
        geo = request.args.get('geo', '')
        timeframe = request.args.get('timeframe', 'today 3-m')
        category = int(request.args.get('category', 0))
        
        # Validate keywords
        if not keywords or keywords[0] == '':
            return jsonify({
                'status': 'error',
                'message': 'Keywords parameter is required'
            }), 400
            
        # Search trends
        results = trends_service.search_trends(
            keywords=keywords,
            geo=geo,
            timeframe=timeframe,
            category=category
        )
        
        return jsonify({
            'status': 'success',
            'data': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@trends_bp.route('/geographic/<region>', methods=['GET'])
def get_regional_trends(region):
    """Get trends for a specific region."""
    try:
        # Get query parameters
        category = int(request.args.get('category', 0))
        resolution = request.args.get('resolution', 'COUNTRY')
        
        # Validate resolution
        valid_resolutions = ['COUNTRY', 'REGION', 'CITY', 'DMA']
        if resolution not in valid_resolutions:
            resolution = 'COUNTRY'
            
        # Get regional trends
        results = trends_service.get_regional_trends(
            region=region,
            category=category,
            resolution=resolution
        )
        
        return jsonify({
            'status': 'success',
            'data': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@trends_bp.route('/history', methods=['GET'])
def get_historical_trends():
    """Get historical trend data."""
    try:
        # Get query parameters
        keywords = request.args.get('keywords', '').split(',')
        geo = request.args.get('geo', '')
        timeframe = request.args.get('timeframe', 'today 5-y')  # Longer timeframe for historical data
        category = int(request.args.get('category', 0))
        
        # Validate keywords
        if not keywords or keywords[0] == '':
            return jsonify({
                'status': 'error',
                'message': 'Keywords parameter is required'
            }), 400
            
        # Search historical trends (reusing search_trends for now)
        results = trends_service.search_trends(
            keywords=keywords,
            geo=geo,
            timeframe=timeframe,
            category=category
        )
        
        return jsonify({
            'status': 'success',
            'data': results
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 