from flask import Blueprint, request, jsonify
from app.models.cup_points import Cup_PointsDAO, Cup_Points
from app.db.db import db

cup_points_bp = Blueprint('cup_points', __name__)

@cup_points_bp.route('/cup_points/<string:game_point_id>', methods=['GET'])
def get_cup_points(game_point_id):
    try:
        cup_point = Cup_PointsDAO.get_cup_points(db, game_point_id)
        if not cup_point:
            return jsonify({"message": "Cup Point not found"}), 404
        return jsonify(cup_point), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @cup_points_bp.route('/cup_points', methods=['GET'])
# def get_all_cup_points():
#     try:
#         cup_points = Cup_PointsDAO.get_all_cup_points(db)
#         if not cup_points:
#             return jsonify({"message": "No cup points found"}), 404
#         return jsonify([point for point in cup_points]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@cup_points_bp.route('/cup_points', methods=['GET'])
def get_paginated_points():
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
        cup_points = Cup_PointsDAO.get_paginated_cup_points(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if cup_points is None:
            return jsonify([]), 200
        return jsonify(cup_points), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@cup_points_bp.route('/cup_points/count', methods=['GET'])
def get_total_points_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            


        total_count = Cup_PointsDAO.get_total_cup_points(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@cup_points_bp.route('/cup_points', methods=['POST'])
def create_cup_points():
    try:
        data = request.get_json()
        point = Cup_Points(**data)
        Cup_PointsDAO.create_cup_points(db, point)
        return jsonify({"message": "Cup point created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_points_bp.route('/cup_points/<string:game_point_id>', methods=['PUT'])
def update_cup_points(game_point_id):
    try:
        data = request.get_json()
        point = Cup_Points(game_point_id=game_point_id, **data)
        Cup_PointsDAO.update_cup_points(db, point)
        return jsonify({"message": "Cup point updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_points_bp.route('/cup_points/<string:game_point_id>', methods=['DELETE'])
def delete_cup_points(game_point_id):
    try:
        Cup_PointsDAO.delete_cup_points(db, game_point_id)
        return jsonify({"message": "Cup point deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# special to POINTS Table 

@cup_points_bp.route('/cup_points/with_year_like', methods=['GET'])
def get_paginated_points_with_like():
    """
    API endpoint for retrieving paginated points with a compulsory 'LIKE' filter on game_point_id.
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
        cup_points = Cup_PointsDAO.get_paginated_cup_points_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if cup_points is None:
            return jsonify([]), 200
        return jsonify(cup_points), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cup_points_bp.route('/cup_points/year_distinct_games', methods=['GET'])
def get_distinct_games_with_like():
    """
    API endpoint for retrieving distinct values of the 'game' column with a compulsory 'LIKE' filter on game_point_id.
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
        distinct_games = Cup_PointsDAO.get_distinct_games_with_like(
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

