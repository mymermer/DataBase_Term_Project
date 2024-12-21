from flask import Blueprint, request, jsonify
from app.models.cup_comparison import Cup_ComparisonDAO, Cup_Comparison
from app.db.db import db

cup_comparison_bp = Blueprint('cup_comparison', __name__)

@cup_comparison_bp.route('/cup_comparison/<string:game_id>', methods=['GET'])
def get_cup_comparison(game_id):
    try:
        cup_comparison = Cup_ComparisonDAO.get_cup_comparison(db, game_id)
        if not cup_comparison:
            return jsonify({"message": "Cup Comparison not found"}), 404
        return jsonify(cup_comparison), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @cup_comparison_bp.route('/cup_comparison', methods=['GET'])
# def get_all_cup_comparison():
#     try:
#         cup_comparison = Cup_ComparisonDAO.get_all_cup_comparison(db)
#         if not cup_comparison:
#             return jsonify({"message": "No cup comparisons found"}), 404
#         return jsonify([comparison for comparison in cup_comparison]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@cup_comparison_bp.route('/cup_comparison', methods=['GET'])
def get_paginated_comparison():
    try:
        offset = int(request.args.get('offset', 0))  # Default to 0 if not provided
        limit = int(request.args.get('limit', 25))  # Default to 25 if not provided
        columns = request.args.get('columns', None)  # Optional column list
        filters_raw = request.args.get('filters', None)  # Optional filters
        sort_by = request.args.get('sortBy', None)  # Optional sort column
        order = request.args.get('order', 'asc')  # Default to ascending order
        
        # Parse columns if provided
        if columns:
            columns = columns.split(",")

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))

        # Call the DAO method with the sort_by and order parameters
        cup_comparison = Cup_ComparisonDAO.get_paginated_cup_comparison(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if cup_comparison is None:
            return jsonify([]), 200
        return jsonify(cup_comparison), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@cup_comparison_bp.route('/cup_comparison/count', methods=['GET'])
def get_total_comparison_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Cup_ComparisonDAO.get_total_cup_comparison(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cup_comparison_bp.route('/cup_comparison', methods=['POST'])
def create_cup_comparison():
    try:
        data = request.get_json()
        comparison = Cup_Comparison(**data)
        Cup_ComparisonDAO.create_cup_comparison(db, comparison)
        return jsonify({"message": "Cup comparison created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_comparison_bp.route('/cup_comparison/<string:game_id>', methods=['PUT'])
def update_cup_comparison(game_id):
    try:
        data = request.get_json()
        comparison = Cup_Comparison(game_id=game_id, **data)
        Cup_ComparisonDAO.update_cup_comparison(db, comparison)
        return jsonify({"message": "Cup comparison updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_comparison_bp.route('/cup_comparison/<string:game_id>', methods=['DELETE'])
def delete_cup_comparison(game_id):
    try:
        Cup_ComparisonDAO.delete_cup_comparison(db, game_id)
        return jsonify({"message": "Cup comparison deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Special routes for COMPARISON Table 

@cup_comparison_bp.route('/cup_comparison/with_year_like', methods=['GET'])
def get_paginated_comparisons_with_like():
    """
    API endpoint for retrieving paginated comparisons with a compulsory 'LIKE' filter on game_id.
    """
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

        offset = int(request.args.get('offset', 0))  # Default to 0 if not provided
        limit = int(request.args.get('limit', 25))  # Default to 25 if not provided
        columns = request.args.get('columns', None)  # Optional column list
        filters_raw = request.args.get('filters', None)  # Optional filters
        sort_by = request.args.get('sortBy', None)  # Optional sort column
        order = request.args.get('order', 'asc')  # Default to ascending order

        # Parse columns if provided
        if columns:
            columns = columns.split(",")

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))

        # Call the DAO method with the like_pattern
        cup_comparisons = Cup_ComparisonDAO.get_paginated_cup_comparison_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if cup_comparisons is None:
            return jsonify([]), 200
        return jsonify(cup_comparisons), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cup_comparison_bp.route('/cup_comparison/year_distinct_games', methods=['GET'])
def get_distinct_comparison_games_with_like():
    """
    API endpoint for retrieving distinct values of the 'game' column with a compulsory 'LIKE' filter on game_id.
    """
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

        columns = request.args.get('columns', None)  # Optional columns to fetch

        # Parse columns if provided
        if columns:
            columns = columns.split(",")

        # Call the DAO method
        distinct_games = Cup_ComparisonDAO.get_distinct_games_with_like(
            db,
            like_pattern=like_pattern,
            columns=columns
        )
        if distinct_games is None:
            return jsonify([]), 200
        return jsonify(distinct_games), 200  # Return the distinct values

    except ValueError:
        return jsonify({'error': 'Invalid columns or likePattern'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
