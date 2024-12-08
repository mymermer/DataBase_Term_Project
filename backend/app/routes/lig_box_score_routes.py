from flask import Blueprint, request, jsonify
from app.models.lig_box_score import LigBoxScoreDAO, LigBoxScore
from app.db.db import db
import logging

# Set up logging
logger = logging.getLogger(__name__)

lig_box_score_bp = Blueprint('lig_box_score', __name__)

# Utility function for standardized responses
def create_response(data=None, message=None, status=200):
    return jsonify({"data": data, "message": message}), status

# Utility function for parsing filters
def parse_filters(filters_raw):
    if filters_raw:
        try:
            return dict(filter.split(":") for filter in filters_raw.split(","))
        except ValueError:
            raise ValueError("Invalid filters format. Expected format: key:value,key2:value2")
    return None

# Route to get a specific lig box score by game_player_id
@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['GET'])
def get_lig_box_score(game_player_id):
    try:
        lig_box_score = LigBoxScoreDAO.get_lig_box_score(db, game_player_id)
        if not lig_box_score:
            return create_response(message="Lig Box Score not found", status=404)
        return create_response(data=lig_box_score, status=200)
    except Exception as e:
        logger.error("Error in get_lig_box_score: %s", str(e))
        return create_response(message="Internal server error", status=500)

# Route to get paginated lig box scores
@lig_box_score_bp.route('/lig_box_score', methods=['GET'])
def get_paginated_box_score():
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 25))
        columns = request.args.get('columns', None)
        filters_raw = request.args.get('filters', None)

        # Validate pagination parameters
        if offset < 0 or limit <= 0:
            return create_response(message="Invalid offset or limit values", status=400)

        # Parse filters and columns
        filters = parse_filters(filters_raw)
        if columns:
            columns = columns.split(",")

        lig_box_scores = LigBoxScoreDAO.get_paginated_lig_box_score(
            db, offset=offset, limit=limit, columns=columns, filters=filters
        )
        return create_response(data=lig_box_scores or [], status=200)
    except ValueError as ve:
        logger.error("Validation error in get_paginated_box_score: %s", str(ve))
        return create_response(message=str(ve), status=400)
    except Exception as e:
        logger.error("Error in get_paginated_box_score: %s", str(e))
        return create_response(message="Internal server error", status=500)

# Route to get the total count of lig box scores
@lig_box_score_bp.route('/lig_box_score/count', methods=['GET'])
def get_total_box_score_count():
    try:
        filters_raw = request.args.get('filters', None)
        filters = parse_filters(filters_raw)

        total_count = LigBoxScoreDAO.get_total_lig_box_score(db, filters=filters)
        return create_response(data={"total": total_count}, status=200)
    except Exception as e:
        logger.error("Error in get_total_box_score_count: %s", str(e))
        return create_response(message="Internal server error", status=500)

# Route to create a new lig box score
@lig_box_score_bp.route('/lig_box_score', methods=['POST'])
def create_lig_box_score():
    try:
        data = request.get_json()
        if not data:
            return create_response(message="Invalid input data", status=400)
        boxscore = LigBoxScore(**data)
        LigBoxScoreDAO.create_lig_box_score(db, boxscore)
        return create_response(message="Lig Box Score created successfully", status=201)
    except Exception as e:
        logger.error("Error in create_lig_box_score: %s", str(e))
        return create_response(message="Internal server error", status=500)

# Route to update a specific lig box score
@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['PUT'])
def update_lig_box_score(game_player_id):
    try:
        data = request.get_json()
        if not data:
            return create_response(message="Invalid input data", status=400)
        boxscore = LigBoxScore(game_player_id=game_player_id, **data)
        LigBoxScoreDAO.update_lig_box_score(db, boxscore)
        return create_response(message="Lig Box Score updated successfully", status=200)
    except Exception as e:
        logger.error("Error in update_lig_box_score: %s", str(e))
        return create_response(message="Internal server error", status=500)

# Route to delete a specific lig box score
@lig_box_score_bp.route('/lig_box_score/<string:game_player_id>', methods=['DELETE'])
def delete_lig_box_score(game_player_id):
    try:
        LigBoxScoreDAO.delete_lig_box_score(db, game_player_id)
        return create_response(message="Lig Box Score deleted successfully", status=200)
    except Exception as e:
        logger.error("Error in delete_lig_box_score: %s", str(e))
        return create_response(message="Internal server error", status=500)
