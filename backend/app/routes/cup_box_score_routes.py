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
        columns = request.args.get('columns', None)  # Optional column list
        filters_raw = request.args.get('filters', None)  # Optional filters
        
        # Parse columns if provided
        if columns:
            columns = columns.split(",")

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))

        cup_box_score = CupBoxScoreDAO.get_paginated_cup_box_score(db, offset=offset, limit=limit, columns=columns, filters=filters)
        if cup_box_score is None:
            return jsonify([]), 200
        return jsonify(cup_box_score), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@cup_box_score_bp.route('/cup_box_score/count', methods=['GET'])
def get_total_box_score_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            


        total_count = CupBoxScoreDAO.get_total_cup_box_score(db,filters=filters)
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
