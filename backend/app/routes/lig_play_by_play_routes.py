from flask import Blueprint, request, jsonify
from app.models.lig_play_by_play import LigPlayByPlayDAO, LigPlayByPlay
from app.db.db import db

lig_play_by_play_bp = Blueprint('lig_play_by_play', __name__)

@lig_play_by_play_bp.route('/lig_play_by_play/<string:game_play_id>', methods=['GET'])
def get_lig_play_by_play(game_play_id):
    try:
        play = LigPlayByPlayDAO.get_play(db, game_play_id)
        if not play:
            return jsonify({"message": "Lig Play not found"}), 404
        return jsonify(play.__dict__), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@lig_play_by_play_bp.route('/lig_play_by_play', methods=['GET'])
def get_paginated_plays():
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

        lig_play_by_play = LigPlayByPlayDAO.get_paginated_plays(db, offset=offset, limit=limit, columns=columns, filters=filters)
        if lig_play_by_play is None:
            return jsonify([]), 200
        return jsonify(lig_play_by_play), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@lig_play_by_play_bp.route('/lig_play_by_play/count', methods=['GET'])
def get_total_play_by_play_count():
    try:
        total_count = LigPlayByPlayDAO.get_total_plays(db)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@lig_play_by_play_bp.route('/lig_play_by_play', methods=['POST'])
def create_lig_play_by_play():
    try:
        data = request.get_json()
        play = LigPlayByPlay(**data)
        LigPlayByPlayDAO.create_play(db, play)
        return jsonify({"message": "Lig Play created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@lig_play_by_play_bp.route('/lig_play_by_play/<string:game_play_id>', methods=['PUT'])
def update_lig_play_by_play(game_play_id):
    try:
        data = request.get_json()
        play = LigPlayByPlay(game_play_id=game_play_id, **data)
        LigPlayByPlayDAO.update_play(db, play)
        return jsonify({"message": "Lig Play updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@lig_play_by_play_bp.route('/lig_play_by_play/<string:game_play_id>', methods=['DELETE'])
def delete_lig_play_by_play(game_play_id):
    try:
        LigPlayByPlayDAO.delete_play(db, game_play_id)
        return jsonify({"message": "Lig Play deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
