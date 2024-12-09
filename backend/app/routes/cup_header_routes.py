from flask import Blueprint, request, jsonify
from app.models.cup_header import Cup_HeaderDAO, Cup_Header
from app.db.db import db

cup_header_bp = Blueprint('cup_header', __name__)

@cup_header_bp.route('/cup_header/<string:game_id>', methods=['GET'])
def get_cup_header(game_id):
    try:
        cup_header = Cup_HeaderDAO.get_cup_header(db, game_id)
        if not cup_header:
            return jsonify({"message": "Cup Header not found"}), 404
        return jsonify(cup_header), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @cup_header_bp.route('/cup_header', methods=['GET'])
# def get_all_cup_header():
#     try:
#         cup_header = Cup_HeaderDAO.get_all_cup_header(db)
#         if not cup_header:
#             return jsonify({"message": "No cup headers found"}), 404
#         return jsonify([header for header in cup_header]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@cup_header_bp.route('/cup_header', methods=['GET'])
def get_paginated_header():
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

        cup_header = Cup_HeaderDAO.get_paginated_cup_header(db, offset=offset, limit=limit, columns=columns, filters=filters)
        if cup_header is None:
            return jsonify([]), 200
        return jsonify(cup_header), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@cup_header_bp.route('/cup_header/count', methods=['GET'])
def get_total_header_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Cup_HeaderDAO.get_total_cup_header(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cup_header_bp.route('/cup_header', methods=['POST'])
def create_cup_header():
    try:
        data = request.get_json()
        header = Cup_Header(**data)
        Cup_HeaderDAO.create_cup_header(db, header)
        return jsonify({"message": "Cup header created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_header_bp.route('/cup_header/<string:game_id>', methods=['PUT'])
def update_cup_header(game_id):
    try:
        data = request.get_json()
        header = Cup_Header(game_id=game_id, **data)
        Cup_HeaderDAO.update_cup_header(db, header)
        return jsonify({"message": "Cup header updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cup_header_bp.route('/cup_header/<string:game_id>', methods=['DELETE'])
def delete_cup_header(game_id):
    try:
        Cup_HeaderDAO.delete_cup_header(db, game_id)
        return jsonify({"message": "Cup header deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500