from flask import Blueprint, request, jsonify
from ..models.kos import Kos
from ..extensions import db
from flask_jwt_extended import jwt_required
from ..utils.decorators import role_required

kos_bp = Blueprint("kos", __name__)

@kos_bp.route("/", methods=["GET"])
def get_all_kos():
    location = request.args.get("location")
    query = Kos.query
    if location:
        query = query.filter(Kos.location.ilike(f"%{location}%"))
    kos_list = query.all()
    return jsonify([{"id": k.id, "name": k.name, "price": k.price, "location": k.location} for k in kos_list])

@kos_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("admin")
def create_kos():
    data = request.get_json()
    kos = Kos(**data)
    db.session.add(kos)
    db.session.commit()
    return jsonify({"msg": "Kos created"}), 201
