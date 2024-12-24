from flask import Blueprint, request, jsonify
from app.models.lig_points import Lig_PointsDAO, Lig_Points
from app.db.db import db

lig_points_bp = Blueprint('lig_points', __name__)

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['GET'])
def get_lig_points(game_point_id):
    try:
        lig_point = Lig_PointsDAO.get_lig_points(db, game_point_id)
        if not lig_point:
            return jsonify({"message": "Lig Point not found"}), 404
        return jsonify(lig_point), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @lig_points_bp.route('/lig_points', methods=['GET'])
# def get_all_lig_points():
#     try:
#         lig_points = Lig_PointsDAO.get_all_lig_points(db)
#         if not lig_points:
#             return jsonify({"message": "No lig points found"}), 404
#         return jsonify([point for point in lig_points]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@lig_points_bp.route('/lig_points', methods=['GET'])
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
        lig_points = Lig_PointsDAO.get_paginated_lig_points(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if lig_points is None:
            return jsonify([]), 200
        return jsonify(lig_points), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@lig_points_bp.route('/lig_points/count', methods=['GET'])
def get_total_points_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            


        total_count = Lig_PointsDAO.get_total_lig_points(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500






@lig_points_bp.route('/lig_points', methods=['POST'])
def create_lig_points():
    try:
        data = request.get_json()
        point = Lig_Points(**data)
        Lig_PointsDAO.create_lig_points(db, point)
        return jsonify({"message": "Lig point created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['PUT'])
def update_lig_points(game_point_id):
    try:
        data = request.get_json()
        point = Lig_Points(game_point_id=game_point_id, **data)
        Lig_PointsDAO.update_lig_points(db, point)
        return jsonify({"message": "Lig point updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['DELETE'])
def delete_lig_points(game_point_id):
    try:
        Lig_PointsDAO.delete_lig_points(db, game_point_id)
        return jsonify({"message": "Lig point deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# special to POINTS Table 

@lig_points_bp.route('/lig_points/with_year_like', methods=['GET'])
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
        lig_points = Lig_PointsDAO.get_paginated_lig_points_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if lig_points is None:
            return jsonify([]), 200
        return jsonify(lig_points), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lig_points_bp.route('/lig_points/year_distinct_games', methods=['GET'])
def get_distinct_games_with_like():
    """
    API endpoint for retrieving distinct values of the 'game' column along with scores, with a compulsory 'LIKE' filter on game_point_id.
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
        distinct_games = Lig_PointsDAO.get_distinct_games_with_like(
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
