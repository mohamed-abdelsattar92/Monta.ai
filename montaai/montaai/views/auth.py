from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import (
    create_access_token,
)
from datetime import timedelta, datetime
from montaai.services.user_service import UserService

import random
import string

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/v1/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username, password, or phone number"}), 400

    result, status_code = UserService.register(username, password)
    return jsonify(result), status_code


@auth_blueprint.route("/v1/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    result, status_code = UserService.login(username, password)
    if status_code != 200:
        return jsonify(result), status_code

    verification_token = "".join(
        random.choices(string.ascii_letters + string.digits, k=32)
    )

    session["username"] = username
    session["verification_token"] = verification_token
    session["verification_token_expiration"] = (
        datetime.utcnow() + timedelta(minutes=10)
    ).isoformat()

    # message = client.messages.create(body=f'Your verification token is: {verification_token}', from_=twilio_from_number, to=user.phone_number)

    # Idealy this can be done through any service like twilio, to send an SMS for actual 2FA.
    return (
        jsonify(
            {"message": f"Verification token {verification_token} sent to {username}"}
        ),
        200,
    )


@auth_blueprint.route("/v1/verify", methods=["POST"])
def verify():
    data = request.get_json()
    username = data.get("username")
    verification_code = data.get("verification_code")

    if not username or not verification_code:
        return jsonify({"error": "Missing username or verification code"}), 400

    verification_username = session.get("username")
    verification_token = session.get("verification_token")
    verification_token_expiration = session.get("verification_token_expiration")
    if (
        not verification_token
        or not verification_token_expiration
        or datetime.utcnow() > datetime.fromisoformat(verification_token_expiration)
    ):
        return jsonify({"error": "Verification token expired or not found"}), 401
    if verification_token and verification_code == verification_token and verification_username == username:
        access_token = create_access_token(
            identity=username, expires_delta=timedelta(minutes=30)
        )
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid verification code"}), 401
