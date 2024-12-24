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
        cup_teams = Cup_TeamsDAO.get_paginated_cup_teams(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )
        if cup_teams is None:
            return jsonify([]), 200
        return jsonify(cup_teams), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@cup_teams_bp.route('/cup_teams/count', methods=['GET'])
def get_total_teams_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            


        total_count = Cup_TeamsDAO.get_total_cup_teams(db,filters=filters)
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


#special to teams

@cup_teams_bp.route('/cup_teams/average-values/<int:season>', methods=['GET'])
def get_average_values(season):
    """
    Fetch the average values for all columns for the given season.
    """
    try:
        averages = Cup_TeamsDAO.get_average_values_by_season(db, season)
        if averages:
            return jsonify({"season": season, "averages": averages}), 200
        return jsonify({"error": "No data found for the provided season."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@cup_teams_bp.route('/cup_teams/with_year_like', methods=['GET'])
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
        cup_teams = Cup_TeamsDAO.get_paginated_cup_teams_with_like(
            db,
            like_pattern=like_pattern,
            offset=offset,
            limit=limit,
            columns=columns,
            filters=filters,
            sort_by=sort_by,
            order=order
        )
        if cup_teams is None:
            return jsonify([]), 200
        return jsonify(cup_teams), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, filters, sortBy, or order'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

@cup_teams_bp.route('/cup_teams/by_team_abbrs', methods=['GET'])
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
        cup_teams_by_abbr = Cup_TeamsDAO.get_paginated_cup_teams_by_abbrs(
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
        for abbr, cup_teams in cup_teams_by_abbr.items():
            response[abbr] = []
            for team in cup_teams:
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

