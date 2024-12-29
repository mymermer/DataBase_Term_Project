from flask import Blueprint, request, jsonify
from app.models.lig_header import Lig_HeaderDAO, Lig_Header
from app.db.db import db

lig_header_bp = Blueprint('lig_header', __name__)

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['GET'])
def get_lig_header(game_id):
    # Fetch the game data
    header = Lig_HeaderDAO.get_lig_header(db, game_id)
    if not header:
        return jsonify({"error": "Game not found"}), 404

    # Return data as a dictionary with "_a" and "_b" suffixes
    response = {
        "game_id": header.game_id,
        "game": header.game,
        "date_of_game": header.date_of_game,
        "time_of_game": header.time_of_game,
        "round_of_game": header.round_of_game,
        "phase": header.phase,
        "season_team_id_a": header.season_team_id_a,
        "season_team_id_b": header.season_team_id_b,
        "score_a": header.score_a,
        "score_b": header.score_b,
        "coach_a": header.coach_a,
        "coach_b": header.coach_b,
        "game_time": header.game_time,
        "referee_1": header.referee_1,
        "referee_2": header.referee_2,
        "referee_3": header.referee_3,
        "stadium": header.stadium,
        "capacity": header.capacity,
        "fouls_a": header.fouls_a,
        "fouls_b": header.fouls_b,
        "timeouts_a": header.timeouts_a,
        "timeouts_b": header.timeouts_b,
        "score_quarter_1_a": header.score_quarter_1_a,
        "score_quarter_2_a": header.score_quarter_2_a,
        "score_quarter_3_a": header.score_quarter_3_a,
        "score_quarter_4_a": header.score_quarter_4_a,
        "score_quarter_1_b": header.score_quarter_1_b,
        "score_quarter_2_b": header.score_quarter_2_b,
        "score_quarter_3_b": header.score_quarter_3_b,
        "score_quarter_4_b": header.score_quarter_4_b,
        "score_extra_time_1_a": header.score_extra_time_1_a,
        "score_extra_time_2_a": header.score_extra_time_2_a,
        "score_extra_time_3_a": header.score_extra_time_3_a,
        "score_extra_time_4_a": header.score_extra_time_4_a,
        "score_extra_time_1_b": header.score_extra_time_1_b,
        "score_extra_time_2_b": header.score_extra_time_2_b,
        "score_extra_time_3_b": header.score_extra_time_3_b,
        "score_extra_time_4_b": header.score_extra_time_4_b,
        "winner": header.winner
    }
    return jsonify(response), 200

@lig_header_bp.route('/lig_header', methods=['GET'])
def get_paginated_header():
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
        lig_header = Lig_HeaderDAO.get_paginated_lig_header(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )        
        if lig_header is None:
            return jsonify([]), 200
        return jsonify(lig_header), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@lig_header_bp.route('/lig_header/count', methods=['GET'])
def get_total_header_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Lig_HeaderDAO.get_total_lig_header(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lig_header_bp.route('/lig_header', methods=['POST'])
def create_lig_header():
    try:
        data = request.get_json()
        header = Lig_Header(**data)
        Lig_HeaderDAO.create_lig_header(db, header)
        return jsonify({"message": "Lig header created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['PUT'])
def update_lig_header(game_id):
    try:
        data = request.get_json()
        header = Lig_Header(game_id=game_id, **data)
        Lig_HeaderDAO.update_lig_header(db, header)
        return jsonify({"message": "Lig header updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['DELETE'])
def delete_lig_header(game_id):
    try:
        Lig_HeaderDAO.delete_lig_header(db, game_id)
        return jsonify({"message": "Lig header deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Special routes for HEADER Table 

@lig_header_bp.route('/lig_header/with_year_like', methods=['GET'])
def get_paginated_headers_with_like():
    """
    API endpoint for retrieving paginated headers with a compulsory 'LIKE' filter on game_id.
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
        lig_headers = Lig_HeaderDAO.get_paginated_lig_header_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if lig_headers is None:
            return jsonify([]), 200
        return jsonify(lig_headers), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@lig_header_bp.route('/lig_header/year_distinct_games', methods=['GET'])
def get_distinct_header_games_with_like():
    """
    API endpoint for retrieving distinct values of the 'game' column along with 'game_id'.
    """
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

        query = """
            SELECT game_id, game FROM LIG_HEADER WHERE game_id LIKE %s
        """
        params = [f"{like_pattern}%"]
        cursor = db.get_connection().cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()

        if not result:
            return jsonify([]), 200
        return jsonify([{"game_id": row[0], "game": row[1]} for row in result]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
