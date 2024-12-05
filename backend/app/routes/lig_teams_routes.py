from flask import Blueprint, request, jsonify
from app.models.lig_teams import Lig_TeamsDAO, Lig_Teams
from app.db.db import db

lig_teams_bp = Blueprint('lig_teams', __name__)

@lig_teams_bp.route('/lig_teams/<string:season_team_id>', methods=['GET'])
def get_lig_teams(season_team_id):
    try:
        lig_team = Lig_TeamsDAO.get_lig_teams(db, season_team_id)
        if not lig_team:
            return jsonify({"message": "Lig Team not found"}), 404
        return jsonify(lig_team), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_teams_bp.route('/lig_teams', methods=['GET'])
def get_all_lig_teams():
    try:
        lig_teams = Lig_TeamsDAO.get_all_lig_teams(db)
        if not lig_teams:
            return jsonify({"message": "No lig teams found"}), 404
        return jsonify([team for team in lig_teams]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_teams_bp.route('/lig_teams', methods=['POST'])
def create_lig_teams():
    try:
        data = request.get_json()
        team = Lig_Teams(**data)
        Lig_TeamsDAO.create_lig_teams(db, team)
        return jsonify({"message": "Lig team created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_teams_bp.route('/lig_teams/<string:season_team_id>', methods=['PUT'])
def update_lig_teams(season_team_id):
    try:
        data = request.get_json()
        team = Lig_Teams(season_team_id=season_team_id, **data)
        Lig_TeamsDAO.update_lig_teams(db, team)
        return jsonify({"message": "Lig team updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_teams_bp.route('/lig_teams/<string:season_team_id>', methods=['DELETE'])
def delete_lig_teams(season_team_id):
    try:
        Lig_TeamsDAO.delete_lig_teams(db, season_team_id)
        return jsonify({"message": "Lig Team deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
