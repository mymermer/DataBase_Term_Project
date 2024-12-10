from flask import Blueprint, request, jsonify
from app.models.team import TeamsDAO, Team
from app.db.db import db


team_bp = Blueprint('team', __name__)

@team_bp.route('/team', methods=['GET'])
def get_team():
    abbreviation = request.args.get('abbreviation')
    full_name = request.args.get('full_name')

    if not abbreviation and not full_name:
        return jsonify({"error": "Either 'abbreviation' or 'full_name' must be provided."}), 400
    
    # Call the DAO to get the team data
    team = TeamsDAO.get_team(db, abbreviation=abbreviation, full_name=full_name)
    
    if team:
        return jsonify({
            "abbreviation": team.abbreviation,
            "full_name": team.full_name,
            "logo_url": team.logo_url
        }), 200
    else:
        return jsonify({"error": "Team not found."}), 404

