from flask import Blueprint, request, jsonify
from app.models.cup_teams import Cup_TeamsDAO, Cup_Teams
from app.db.db import db

cup_teams_bp = Blueprint('cup_teams', __name__)

@cup_teams_bp.route('/cup_teams/<string:season_team_id>', methods=['GET'])
def get_cup_teams(season_team_id):
    try:
        cup_team = Cup_TeamsDAO.get_cup_teams(db, season_team_id)
        if not cup_team:
            return jsonify({"message": "Cup Team not found"}), 404
        return jsonify(cup_team), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @cup_teams_bp.route('/cup_teams', methods=['GET'])
# def get_all_cup_teams():
#     try:
#         cup_teams = Cup_TeamsDAO.get_all_cup_teams(db)
#         if not cup_teams:
#             return jsonify({"message": "No cup teams found"}), 404
#         return jsonify([team for team in cup_teams]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@cup_teams_bp.route('/cup_teams', methods=['GET'])
def get_paginated_teams():
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

        cup_teams = Cup_TeamsDAO.get_paginated_cup_teams(db, offset=offset, limit=limit, columns=columns, filters=filters)
        if cup_teams is None:
            return jsonify([]), 200
        return jsonify(cup_teams), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@cup_teams_bp.route('/cup_teams/count', methods=['GET'])
def get_total_teams_count():
    try:
        total_count = Cup_TeamsDAO.get_total_cup_teams(db)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cup_teams_bp.route('/cup_teams', methods=['POST'])
def create_cup_teams():
    try:
        data = request.get_json()
        team = Cup_Teams(**data)
        Cup_TeamsDAO.create_cup_teams(db, team)
        return jsonify({"message": "Cup team created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_teams_bp.route('/cup_teams/<string:season_team_id>', methods=['PUT'])
def update_cup_teams(season_team_id):
    try:
        data = request.get_json()
        team = Cup_Teams(season_team_id=season_team_id, **data)
        Cup_TeamsDAO.update_cup_teams(db, team)
        return jsonify({"message": "Cup team updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_teams_bp.route('/cup_teams/<string:season_team_id>', methods=['DELETE'])
def delete_cup_teams(season_team_id):
    try:
        Cup_TeamsDAO.delete_cup_teams(db, season_team_id)
        return jsonify({"message": "Cup Team deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
