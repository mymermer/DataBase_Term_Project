from flask import Blueprint, request, jsonify
from app.models.cup_box_score import CupBoxScoreDAO, CupBoxScore
from app.db.db import db

cup_box_score_bp = Blueprint('cup_box_score', __name__)

@cup_box_score_bp.route('/cup_box_score/<string:game_player_id>', methods=['GET'])
def get_cup_box_score(game_player_id):
    try:
        cup_box_score = CupBoxScoreDAO.get_cup_box_score(db, game_player_id)
        if not cup_box_score:
            return jsonify({"message": "Cup Box Score not found"}), 404
        return jsonify(cup_box_score), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cup_box_score_bp.route('/cup_box_score', methods=['GET'])
def get_paginated_box_score():
    try:
        offset = int(request.args.get('offset', 0))  # Default to 0 if not provided
        limit = int(request.args.get('limit', 25))  # Default to 25 if not provided
        columns = request.args.get('columns', None)  
        filters_raw = request.args.get('filters', None)  
        sort_by = request.args.get('sortBy', None)  
        order = request.args.get('order', 'asc') 
        
       
        if columns:
            columns = columns.split(",")

       
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(";"))

        cup_box_score = CupBoxScoreDAO.get_paginated_cup_box_scores(
            db, 
            offset=offset, 
            limit=limit,
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )    
        if cup_box_score is None:
            return jsonify([]), 200
        return jsonify(cup_box_score), 200  
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@cup_box_score_bp.route('/cup_box_score/count', methods=['GET'])
def get_total_box_score_count():
    try:
        filters_raw = request.args.get('filters', None)  
        
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(";"))

        total_count = CupBoxScoreDAO.get_total_cup_box_scores(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cup_box_score_bp.route('/cup_box_score', methods=['POST'])
def create_cup_box_score():
    try:
        data = request.get_json()
        boxscore = CupBoxScore(**data)
        CupBoxScoreDAO.create_cup_box_score(db, boxscore)
        return jsonify({"message": "Cup box score created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_box_score_bp.route('/cup_box_score/<string:game_player_id>', methods=['PUT'])
def update_cup_box_score(game_player_id):
    try:
        data = request.get_json()
        boxscore = CupBoxScore(game_player_id=game_player_id, **data)
        CupBoxScoreDAO.update_cup_box_score(db, boxscore)
        return jsonify({"message": "Cup Box Score updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_box_score_bp.route('/cup_box_score/<string:game_player_id>', methods=['DELETE'])
def delete_cup_box_score(game_player_id):
    try:
        CupBoxScoreDAO.delete_cup_box_score(db, game_player_id)
        return jsonify({"message": "Cup Box Score deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@cup_box_score_bp.route('/cup_box_score/with_year_like', methods=['GET'])
def get_filtered_box_score_with_like():
    """
    API endpoint for retrieving filtered plays with a compulsory 'LIKE' filter on game_play_id.
    """
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

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
        cup_box_score = CupBoxScoreDAO.get_filtered_cup_box_score_with_like(
            db,
            like_pattern=like_pattern,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if cup_box_score is None:
            return jsonify([]), 200
        return jsonify(cup_box_score), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@cup_box_score_bp.route('/cup_box_score/year_distinct_games', methods=['GET'])
def get_distinct_games_with_like():
    """
    GET /cup_box_score/year_distinct_games?likePattern=E2007
    -> Returns distinct 'game' values from CUP_BOX_SCORE
       where game_id LIKE 'E2007%'
    """
    try:
        like_pattern = request.args.get('likePattern', None)
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. Must be at least 5 characters.'}), 400

        # columns param optional, just like the play_by_play
        columns = request.args.get('columns', None)
        if columns:
            columns = columns.split(",")

        # Now call a DAO method that does a query for distinct games
        distinct_games = CupBoxScoreDAO.get_distinct_games_with_like(
            db, 
            like_pattern=like_pattern,
            columns=columns
        )
        if distinct_games is None:
            return jsonify([]), 200
        return jsonify(distinct_games), 200

    except ValueError:
        return jsonify({'error': 'Invalid columns or likePattern'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
    
    
    
