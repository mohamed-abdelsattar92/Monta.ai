from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
)
from datetime import timedelta

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if username == "admin" and password == "admin":
        access_token = create_access_token(
            identity=username, expires_delta=timedelta(minutes=30)
        )
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401