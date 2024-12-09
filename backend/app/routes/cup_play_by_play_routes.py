from flask import Blueprint, request, jsonify
from app.models.cup_play_by_play import CupPlayByPlayDAO, CupPlayByPlay
from app.db.db import db

cup_play_by_play_bp = Blueprint('cup_play_by_play', __name__)

@cup_play_by_play_bp.route('/cup_play_by_play/<string:game_play_id>', methods=['GET'])
def get_cup_play_by_play(game_play_id):
    try:
        play = CupPlayByPlayDAO.get_play(db, game_play_id)
        if not play:
            return jsonify({"message": "Cup Play not found"}), 404
        return jsonify(play.__dict__), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@cup_play_by_play_bp.route('/cup_play_by_play', methods=['GET'])
def get_paginated_points():
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

        cup_play_by_play = CupPlayByPlayDAO.get_paginated_cup_play_by_play(db, offset=offset, limit=limit, columns=columns, filters=filters)
        if cup_play_by_play is None:
            return jsonify([]), 200
        return jsonify(cup_play_by_play), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@cup_play_by_play_bp.route('/cup_play_by_play/count', methods=['GET'])
def get_total_points_count():
    try:
        total_count = CupPlayByPlayDAO.get_total_cup_points(db)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@cup_play_by_play_bp.route('/cup_play_by_play', methods=['POST'])
def create_cup_play_by_play():
    try:
        data = request.get_json()
        play = CupPlayByPlay(**data)
        CupPlayByPlayDAO.create_play(db, play)
        return jsonify({"message": "Cup Play created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@cup_play_by_play_bp.route('/cup_play_by_play/<string:game_play_id>', methods=['PUT'])
def update_cup_play_by_play(game_play_id):
    try:
        data = request.get_json()
        play = CupPlayByPlay(game_play_id=game_play_id, **data)
        CupPlayByPlayDAO.update_play(db, play)
        return jsonify({"message": "Cup Play updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@cup_play_by_play_bp.route('/cup_play_by_play/<string:game_play_id>', methods=['DELETE'])
def delete_cup_play_by_play(game_play_id):
    try:
        CupPlayByPlayDAO.delete_play(db, game_play_id)
        return jsonify({"message": "Cup Play deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
