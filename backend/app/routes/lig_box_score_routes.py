from flask import Blueprint, request, jsonify
from app.models.lig_box_score import LigBoxScoreDAO, LigBoxScore
from app.db.db import db

lig_box_score_bp = Blueprint('lig_box_score', __name__)

@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['GET'])
def get_lig_box_score(game_player_id):
    try:
        lig_box_score = LigBoxScoreDAO.get_lig_box_score(db, game_player_id)
        if not lig_box_score:
            return jsonify({"message": "Lig box score not found"}), 404
        return jsonify(lig_box_score), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@lig_box_score_bp.route('/lig_box_score', methods=['GET'])
def get_paginated_box_score():
    try:
        offset = int(request.args.get('offset', 0)) 
        limit = int(request.args.get('limit', 25))  
        columns = request.args.get('columns', None)  
        filters_raw = request.args.get('filters', None) 
        sort_by = request.args.get('sortBy', None)  
        order = request.args.get('order', 'asc')  

        
        if columns:
            columns = columns.split(",")

        
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))

        
        lig_box_score = LigBoxScoreDAO.get_paginated_lig_box_scores(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if lig_box_score is None:
            return jsonify([]), 200
        return jsonify(lig_box_score), 200  
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@lig_box_score_bp.route('/lig_box_score/count', methods=['GET'])
def get_total_box_score_count():
    try:
        filters_raw = request.args.get('filters', None) 

        
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = LigBoxScoreDAO.get_total_lig_box_scores(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@lig_box_score_bp.route('/lig_box_score', methods=['POST'])
def create_lig_box_score():
    try:
        data = request.get_json()
        boxscore = LigBoxScore(**data)
        LigBoxScoreDAO.create_lig_box_score(db, boxscore)
        return jsonify({"message": "Lig box score created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['PUT'])
def update_lig_box_score(game_player_id):
    try:
        data = request.get_json()
        boxscore = LigBoxScore(game_player_id=game_player_id, **data)
        LigBoxScoreDAO.update_lig_box_score(db, boxscore)
        return jsonify({"message": "Lig box score updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['DELETE'])
def delete_lig_box_score(game_player_id):
    try:
        LigBoxScoreDAO.delete_lig_box_score(db, game_player_id)
        return jsonify({"message": "Lig box score deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500







