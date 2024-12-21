from flask import Blueprint, request, jsonify
from app.models.lig_comparison import Lig_ComparisonDAO, Lig_Comparison
from app.db.db import db

lig_comparison_bp = Blueprint('lig_comparison', __name__)

@lig_comparison_bp.route('/lig_comparison/<string:game_id>', methods=['GET'])
def get_lig_comparison(game_id):
    try:
        lig_comparison = Lig_ComparisonDAO.get_lig_comparison(db, game_id)
        if not lig_comparison:
            return jsonify({"message": "Lig Comparison not found"}), 404
        return jsonify(lig_comparison), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @lig_comparison_bp.route('/lig_comparison', methods=['GET'])
# def get_all_lig_comparison():
#     try:
#         lig_comparison = Lig_ComparisonDAO.get_all_lig_comparison(db)
#         if not lig_comparison:
#             return jsonify({"message": "No lig comparisons found"}), 404
#         return jsonify([comparison for comparison in lig_comparison]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@lig_comparison_bp.route('/lig_comparison', methods=['GET'])
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
        lig_comparison = Lig_ComparisonDAO.get_paginated_lig_comparison(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if lig_comparison is None:
            return jsonify([]), 200
        return jsonify(lig_comparison), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@lig_comparison_bp.route('/lig_comparison/count', methods=['GET'])
def get_total_comparison_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Lig_ComparisonDAO.get_total_lig_comparison(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lig_comparison_bp.route('/lig_comparison', methods=['POST'])
def create_lig_comparison():
    try:
        data = request.get_json()
        comparison = Lig_Comparison(**data)
        Lig_ComparisonDAO.create_lig_comparison(db, comparison)
        return jsonify({"message": "Lig comparison created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_comparison_bp.route('/lig_comparison/<string:game_id>', methods=['PUT'])
def update_lig_comparison(game_id):
    try:
        data = request.get_json()
        comparison = Lig_Comparison(game_id=game_id, **data)
        Lig_ComparisonDAO.update_lig_comparison(db, comparison)
        return jsonify({"message": "Lig comparison updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_comparison_bp.route('/lig_comparison/<string:game_id>', methods=['DELETE'])
def delete_lig_comparison(game_id):
    try:
        Lig_ComparisonDAO.delete_lig_comparison(db, game_id)
        return jsonify({"message": "Lig comparison deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Special routes for COMPARISON Table 

@lig_comparison_bp.route('/lig_comparison/with_year_like', methods=['GET'])
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
        lig_comparisons = Lig_ComparisonDAO.get_paginated_lig_comparison_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if lig_comparisons is None:
            return jsonify([]), 200
        return jsonify(lig_comparisons), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lig_comparison_bp.route('/lig_comparison/year_distinct_games', methods=['GET'])
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
        distinct_games = Lig_ComparisonDAO.get_distinct_games_with_like(
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
