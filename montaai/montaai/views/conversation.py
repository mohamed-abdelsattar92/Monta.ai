from uuid import UUID, uuid4

import openai
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from montaai.helpers import chat_history

openai_client = openai.OpenAI()

conversation_blueprint = Blueprint("conversation", __name__)


@conversation_blueprint.route("/conversation", methods=["POST"])
@jwt_required()
def create_new_conversation():
    user_id = get_jwt_identity()
    new_conversation_id = uuid4()
    if user_id not in chat_history:
        chat_history[user_id] = {}
    chat_history[user_id][str(new_conversation_id)] = []
    return (
        jsonify(
            {"message": f"New conversation created with id: {new_conversation_id}"}
        ),
        200,
    )


@conversation_blueprint.route("/conversation/<uuid:id>", methods=["GET"])
@jwt_required()
def get_conversation(id: UUID):
    user_id = get_jwt_identity()
    try:
        conversation = chat_history[user_id][str(id)]
        return jsonify({f"{id}": conversation}), 200
    except KeyError:
        return jsonify({"error": "Conversation not found"}), 404
    except Exception as e:
        return jsonify({"Error": f"{e}"})


@conversation_blueprint.route("/conversation/<uuid:conversation_id>/message", methods=["POST"])
@jwt_required()
def send_message(conversation_id: UUID):
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Message can't be empty"}), 400

    user_id = get_jwt_identity()
    conversation_context = chat_history.get(user_id, {}).get(str(conversation_id))
    if conversation_context is None:
        return jsonify({"error": "Please enter the correct conversation id!"}), 404
    conversation_context.append({"role": "user", "content": user_input})

    try:
        completions = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_context,
        )
        conversation_context.append(
            {
                "role": completions.choices[0].message.role,
                "content": completions.choices[0].message.content,
            }
        )
        return jsonify({"response": completions.choices[0].message.content}), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Our Service is currently down and we're working on get it back up shortly, please try again later! Thanks for you patience"
                }
            ),
            500,
        )


@conversation_blueprint.route("/history", methods=["GET"])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    user_history = chat_history.get(user_id, [])
    return jsonify({"history": user_history}), 200
