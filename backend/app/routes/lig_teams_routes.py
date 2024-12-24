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

# @lig_teams_bp.route('/lig_teams', methods=['GET'])
# def get_all_lig_teams():
#     try:
#         lig_teams = Lig_TeamsDAO.get_all_lig_teams(db)
#         if not lig_teams:
#             return jsonify({"message": "No lig teams found"}), 404
#         return jsonify([team for team in lig_teams]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@lig_teams_bp.route('/lig_teams', methods=['GET'])
def get_paginated_teams():
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
        lig_teams = Lig_TeamsDAO.get_paginated_lig_teams(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if lig_teams is None:
            return jsonify([]), 200
        return jsonify(lig_teams), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@lig_teams_bp.route('/lig_teams/count', methods=['GET'])
def get_total_teams_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            


        total_count = Lig_TeamsDAO.get_total_lig_teams(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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


#special to teams

@lig_teams_bp.route('/lig_teams/average-values/<int:season>', methods=['GET'])
def get_average_values(season):
    """
    Fetch the average values for all columns for the given season.
    """
    try:
        averages = Lig_TeamsDAO.get_average_values_by_season(db, season)
        if averages:
            return jsonify({"season": season, "averages": averages}), 200
        return jsonify({"error": "No data found for the provided season."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@lig_teams_bp.route('/lig_teams/with_year_like', methods=['GET'])
def get_paginated_teams_with_like():
    try:
        # Retrieve query parameters
        like_pattern = request.args.get('likePattern', None)  # The LIKE pattern (e.g., "ABCDE%")
        if not like_pattern or len(like_pattern) < 5:
            return jsonify({'error': 'Invalid likePattern. It must be at least 5 characters long.'}), 400

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

        # Call the DAO method with the like_pattern
        lig_teams = Lig_TeamsDAO.get_paginated_lig_teams_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if lig_teams is None:
            return jsonify([]), 200
        return jsonify(lig_teams), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@lig_teams_bp.route('/lig_teams/by_team_abbrs', methods=['GET'])
def get_paginated_teams_by_abbrs():
    try:
        # Retrieve query parameters
        team_abbrs_raw = request.args.get('teamAbbrs', None)  # Comma-separated list of abbreviations
        if not team_abbrs_raw:
            return jsonify({'error': 'teamAbbrs parameter is required and cannot be empty.'}), 400
        
        team_abbrs = team_abbrs_raw.split(',')
        team_abbrs = [abbr.strip() for abbr in team_abbrs if len(abbr.strip()) == 3]
        if not team_abbrs:
            return jsonify({'error': 'All team abbreviations must be exactly 3 characters long.'}), 400

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

        # Call the DAO method with the list of team abbreviations
        lig_teams_by_abbr = Lig_TeamsDAO.get_paginated_lig_teams_by_abbrs(
            db,
            team_abbrs=team_abbrs,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )

        # Add year information to each row and separate by abbreviation
        response = {}
        for abbr, lig_teams in lig_teams_by_abbr.items():
            response[abbr] = []
            for team in lig_teams:
                season_team_id = team.get('season_team_id', '')
                if len(season_team_id) >= 9:
                    year = season_team_id[1:5]  # Extract year
                    team['year'] = year
                response[abbr].append(team)

        return jsonify(response), 200  # Structured by team abbreviation
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
