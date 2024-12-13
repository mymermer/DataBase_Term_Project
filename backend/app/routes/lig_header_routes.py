from flask import Blueprint, request, jsonify
from app.models.lig_header import Lig_HeaderDAO, Lig_Header
from app.db.db import db

lig_header_bp = Blueprint('lig_header', __name__)

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['GET'])
def get_lig_header(game_id):
    try:
        lig_header = Lig_HeaderDAO.get_lig_header(db, game_id)
        if not lig_header:
            return jsonify({"message": "Lig Header not found"}), 404
        return jsonify(lig_header), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @lig_header_bp.route('/lig_header', methods=['GET'])
# def get_all_lig_header():
#     try:
#         lig_header = Lig_HeaderDAO.get_all_lig_header(db)
#         if not lig_header:
#             return jsonify({"message": "No lig headers found"}), 404
#         return jsonify([header for header in lig_header]), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@lig_header_bp.route('/lig_header', methods=['GET'])
def get_paginated_header():
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
        lig_header = Lig_HeaderDAO.get_paginated_lig_header(
            db, 
            offset=offset, 
            limit=limit, 
            columns=columns, 
            filters=filters, 
            sort_by=sort_by, 
            order=order
        )        
        if lig_header is None:
            return jsonify([]), 200
        return jsonify(lig_header), 200  # Already a list of dicts if columns are specified
    except ValueError:
        return jsonify({'error': 'Invalid offset, limit, columns, or filters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@lig_header_bp.route('/lig_header/count', methods=['GET'])
def get_total_header_count():
    try:
        filters_raw = request.args.get('filters', None)  # Optional filters

        # Parse filters if provided
        filters = None
        if filters_raw:
            filters = dict(filter.split(":") for filter in filters_raw.split(","))
            
        total_count = Lig_HeaderDAO.get_total_lig_header(db,filters=filters)
        return jsonify({'total': total_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lig_header_bp.route('/lig_header', methods=['POST'])
def create_lig_header():
    try:
        data = request.get_json()
        header = Lig_Header(**data)
        Lig_HeaderDAO.create_lig_header(db, header)
        return jsonify({"message": "Lig header created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['PUT'])
def update_lig_header(game_id):
    try:
        data = request.get_json()
        header = Lig_Header(game_id=game_id, **data)
        Lig_HeaderDAO.update_lig_header(db, header)
        return jsonify({"message": "Lig header updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_header_bp.route('/lig_header/<string:game_id>', methods=['DELETE'])
def delete_lig_header(game_id):
    try:
        Lig_HeaderDAO.delete_lig_header(db, game_id)
        return jsonify({"message": "Lig header deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500