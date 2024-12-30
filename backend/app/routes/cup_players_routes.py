from flask import Blueprint, request, jsonify
from app.models.cup_players import Cup_PlayersDAO, Cup_Player
from app.db.db import db

cup_players_bp = Blueprint('cup_players', __name__)

@cup_players_bp.route('/cup_players/<string:season_player_id>', methods=['GET'])
def get_cup_players(season_player_id):
    try:
        cup_player = Cup_PlayersDAO.get_cup_player(db, season_player_id)
        if not cup_player:
            return jsonify({"message": "Cup Player not found"}), 404
        return jsonify(cup_player), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@cup_players_bp.route('/cup_players', methods=['GET'])
def get_paginated_players():
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
        cup_players = Cup_PlayersDAO.get_paginated_cup_players(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if cup_players is None:
            return jsonify([]), 200
        return jsonify(cup_players), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({"error': 'Invalid offset, limit, columns, filters, sortBy, or order"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@cup_players_bp.route('/cup_players', methods=['POST'])
def create_cup_players():
    try:
        data = request.get_json()
        cup_player = Cup_Player(**data)
        Cup_PlayersDAO.create_cup_players(db, cup_player)
        return jsonify({"message": "Cup player created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@cup_players_bp.route('/cup_players/<string:season_player_id>', methods=['PUT'])
def update_cup_players(season_player_id):
    try:
        data = request.get_json()
        cup_player = Cup_Player(season_player_id=season_player_id, **data)
        Cup_PlayersDAO.update_cup_player(db, cup_player)
        return jsonify({"message": "Cup player updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@cup_players_bp.route('/cup_players/<string:season_player_id>', methods=['DELETE'])
def delete_cup_players(season_player_id):
    try:
        Cup_PlayersDAO.delete_player(db, season_player_id)
        return jsonify({"message": "Cup player deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@cup_players_bp.route('/cup_players/count', methods=['GET'])
def get_total_cup_players():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Cup_PlayersDAO.get_total_cup_players(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@cup_players_bp.route('/cup_players/<string:season>/teams', methods=['GET'])
def get_distinct_teams_by_year(season):
    try:
        teams = Cup_PlayersDAO.get_distinct_teams_by_year(db, season)
        return jsonify(teams), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@cup_players_bp.route('/cup_players/<string:season>/<string:team>/player_percentages', methods=['GET'])
def get_player_percentages_by_team_and_season(season, team):
    try:
        player_percentages = Cup_PlayersDAO.get_players_point_percentage_by_team_and_season(db, season, team)
        return jsonify(player_percentages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500