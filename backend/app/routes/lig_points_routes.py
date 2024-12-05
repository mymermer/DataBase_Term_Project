from flask import Blueprint, request, jsonify
from app.models.lig_points import Lig_PointsDAO, Lig_Points
from app.db.db import db

lig_points_bp = Blueprint('lig_points', __name__)

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['GET'])
def get_lig_points(game_point_id):
    try:
        lig_point = Lig_PointsDAO.get_lig_points(db, game_point_id)
        if not lig_point:
            return jsonify({"message": "Lig Point not found"}), 404
        return jsonify(lig_point), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points', methods=['GET'])
def get_all_lig_points():
    try:
        lig_points = Lig_PointsDAO.get_all_lig_points(db)
        if not lig_points:
            return jsonify({"message": "No lig points found"}), 404
        return jsonify([point for point in lig_points]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points', methods=['POST'])
def create_lig_points():
    try:
        data = request.get_json()
        point = Lig_Points(**data)
        Lig_PointsDAO.create_lig_points(db, point)
        return jsonify({"message": "Lig point created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['PUT'])
def update_lig_points(game_point_id):
    try:
        data = request.get_json()
        point = Lig_Points(game_point_id=game_point_id, **data)
        Lig_PointsDAO.update_lig_points(db, point)
        return jsonify({"message": "Lig point updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@lig_points_bp.route('/lig_points/<string:game_point_id>', methods=['DELETE'])
def delete_lig_points(game_point_id):
    try:
        Lig_PointsDAO.delete_lig_points(db, game_point_id)
        return jsonify({"message": "Lig point deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
