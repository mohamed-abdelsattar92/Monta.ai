from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
)
from datetime import timedelta

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/v1/login", methods=["POST"])
def login():
    allowed_users = {"admin", "user1", "user2", "user3"}
    username = request.json.get("username")
    password = request.json.get("password")

    if username in allowed_users and password == "admin":
        access_token = create_access_token(
            identity=username, expires_delta=timedelta(minutes=30)
        )
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401