from flask import Blueprint, request, jsonify
from app.models.cup_comparison import Cup_ComparisonDAO, Cup_Comparison
from app.db.db import db

cup_comparison_bp = Blueprint('cup_comparison', __name__)

# game_id VARCHAR(50) PRIMARY KEY,
# game VARCHAR(50),
# round_of_game INT,
# phase VARCHAR(50),
# season_team_id_a VARCHAR(50),
# season_team_id_b VARCHAR(50),
# fast_break_points_a INT,
# fast_break_points_b INT,
# turnover_points_a INT,
# turnover_points_b INT,
# second_chance_points_a INT,
# second_chance_points_b INT,
# defensive_rebounds_a INT,
# offensive_rebounds_b INT,
# offensive_rebounds_a INT,
# defensive_rebounds_b INT,
# turnovers_starters_a INT,
# turnovers_bench_a INT,
# turnovers_starters_b INT,
# turnovers_bench_b INT,
# steals_starters_a INT,
# steals_bench_a INT,
# steals_starters_b INT,
# steals_bench_b INT,
# assists_starters_a INT,
# assists_bench_a INT,
# assists_starters_b INT,
# assists_bench_b INT,
# points_starters_a INT,
# points_bench_a INT,
# points_starters_b INT,
# points_bench_b INT,
# max_lead_a INT,
# max_lead_b INT,
# minute_max_lead_a INT,
# minute_max_lead_b INT,
# points_max_lead_a VARCHAR(50),
# points_max_lead_b VARCHAR(50)

@cup_comparison_bp.route('/cup_comparison/<string:game_id>', methods=['GET'])
def get_cup_comparison(game_id):
    # Fetch the game data
    comparison = Cup_ComparisonDAO.get_cup_comparison(db, game_id)
    if not comparison:
        return jsonify({"error": "Game not found"}), 404

    # Return data as a dictionary with "_a" and "_b" suffixes
    response = {
        "game_id": comparison.game_id,
        "game": comparison.game,
        "round_of_game": comparison.round_of_game,
        "phase": comparison.phase,
        "season_team_id_a": comparison.season_team_id_a,
        "season_team_id_b": comparison.season_team_id_b,
        "fast_break_points_a": comparison.fast_break_points_a,
        "fast_break_points_b": comparison.fast_break_points_b,
        "turnover_points_a": comparison.turnover_points_a,
        "turnover_points_b": comparison.turnover_points_b,
        "second_chance_points_a": comparison.second_chance_points_a,
        "second_chance_points_b": comparison.second_chance_points_b,
        "defensive_rebounds_a": comparison.defensive_rebounds_a,
        "offensive_rebounds_b": comparison.offensive_rebounds_b,
        "offensive_rebounds_a": comparison.offensive_rebounds_a,
        "defensive_rebounds_b": comparison.defensive_rebounds_b,
        "turnovers_starters_a": comparison.turnovers_starters_a,
        "turnovers_bench_a": comparison.turnovers_bench_a,
        "turnovers_starters_b": comparison.turnovers_starters_b,
        "turnovers_bench_b": comparison.turnovers_bench_b,
        "steals_starters_a": comparison.steals_starters_a,
        "steals_bench_a": comparison.steals_bench_a,
        "steals_starters_b": comparison.steals_starters_b,
        "steals_bench_b": comparison.steals_bench_b,
        "assists_starters_a": comparison.assists_starters_a,
        "assists_bench_a": comparison.assists_bench_a,
        "assists_starters_b": comparison.assists_starters_b,
        "assists_bench_b": comparison.assists_bench_b,
        "points_starters_a": comparison.points_starters_a,
        "points_bench_a": comparison.points_bench_a,
        "points_starters_b": comparison.points_starters_b,
        "points_bench_b": comparison.points_bench_b,
        "max_lead_a": comparison.max_lead_a,
        "max_lead_b": comparison.max_lead_b,
        "minute_max_lead_a": comparison.minute_max_lead_a,
        "minute_max_lead_b": comparison.minute_max_lead_b,
        "points_max_lead_a": comparison.points_max_lead_a,
        "points_max_lead_b": comparison.points_max_lead_b
    }
    return jsonify(response), 200

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
    API endpoint for retrieving distinct values of the 'game' column along with 'game_id'.
    """
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

        query = """
            SELECT game_id, game FROM CUP_COMPARISON WHERE game_id LIKE %s
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
