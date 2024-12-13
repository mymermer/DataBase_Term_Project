from flask import Blueprint, request, jsonify
from app.models.team import TeamsDAO, Team
from app.db.db import db


team_bp = Blueprint('team', __name__)

@team_bp.route('/team', methods=['GET'])
def get_team():
    abbreviations = request.args.get('abbreviation')
    full_names = request.args.get('full_name')

    if not abbreviations and not full_names:
        return jsonify({"error": "Either 'abbreviation' or 'full_name' must be provided."}), 400

    # Split comma-separated values into lists
    abbreviation_list = abbreviations.split(',') if abbreviations else []
    full_name_list = full_names.split(',') if full_names else []

    # Call the DAO to get the team data
    try:
        teams = TeamsDAO.get_teams(
            db,
            abbreviations=abbreviation_list,
            full_names=full_name_list
        )
        if teams:
            return jsonify([
                {
                    "abbreviation": team.abbreviation,
                    "full_name": team.full_name,
                    "logo_url": team.logo_url
                } for team in teams
            ]), 200
        else:
            return jsonify({"error": "No matching teams found."}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


