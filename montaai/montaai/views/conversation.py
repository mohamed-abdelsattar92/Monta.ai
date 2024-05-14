import openai
import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from montaai.helpers.database import redis_client, db
from montaai.models.conversations import Conversation
from montaai.models.messages import Message
from montaai.models.users import User

openai_client = openai.OpenAI()

conversation_blueprint = Blueprint("conversation", __name__)


@conversation_blueprint.route("/v1/conversation", methods=["POST"])
@jwt_required()
def create_new_conversation():
    user_id = get_jwt_identity()
    user_object = User.query.filter_by(username=user_id).first()

    current_conversation_key = f"conversation:{user_id}:current"
    current_conversation = redis_client.get(current_conversation_key)

    if current_conversation:
        conversation_data = json.loads(current_conversation.decode("utf-8"))

        existing_conversation: Conversation = Conversation.query.filter_by(
            id=conversation_data["id"]
        ).first()

        if existing_conversation:
            existing_conversation.messages = conversation_data["messages"]
        else:
            new_db_conversation_for_current_conversation = Conversation(user_id=user_object.id)
            db.session.add(new_db_conversation_for_current_conversation)

            for message in conversation_data["messages"]:
                new_db_message = Message(
                    conversation_id=new_db_conversation_for_current_conversation.id,
                    role=message["role"],
                    content=message["content"],
                )
                db.session.add(new_db_message)
                
    new_db_conversation = Conversation(user_id=user_object.id)
    db.session.add(new_db_conversation)
    db.session.commit()

    new_conversation_data = {"id": str(new_db_conversation.id), "messages": []}
    redis_client.setex(current_conversation_key, json.dumps(new_conversation_data))

    return (
        jsonify(
            {"message": f"New conversation created with id: {new_db_conversation.id}"}
        ),
        200,
    )


@conversation_blueprint.route("/v1/conversation/<int:id>", methods=["GET"])
@jwt_required()
def get_conversation(id: int):
    user_id = get_jwt_identity()
    user_object = User.query.filter_by(username=user_id).first()

    conversation = Conversation.query.filter_by(id=str(id)).first()

    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    messages: Message = Message.query.filter_by(conversation_id=conversation.id).all()
    conversation_history = [
        {"role": message.role, "content": message.content} for message in messages
    ]

    conversation_key = f"conversation:{user_id}:current"
    redis_client.setex(conversation_key, json.dumps(conversation_history))

    return jsonify({f"{id}": conversation_history}), 200


@conversation_blueprint.route("/v1/conversation/message", methods=["POST"])
@jwt_required()
def send_message():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Message can't be empty"}), 400

    user_id = get_jwt_identity()
    conversation_key = f"conversation:{user_id}:current"
    conversation_context = redis_client.get(conversation_key)

    if not conversation_context:
        return jsonify({"error": "Please enter the correct conversation id!"}), 404

    conversation_context = json.loads(conversation_context.decode("utf-8"))

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

        redis_client.setex(conversation_key, json.dumps(conversation_context))

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


@conversation_blueprint.route("/v1/conversations", methods=["GET"])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    user_object = User.query.filter_by(username=user_id).first()

    db_conversations = Conversation.query.filter_by(user_id=user_object.id).all()

    conversation_history = []

    for conversation in db_conversations:
        messages = Message.query.filter_by(conversation_id=conversation.id).all()
        conversation_history.append(
            {
                "conversation_id": conversation.id,
                "messages": [
                    {"role": message.role, "content": message.content}
                    for message in messages
                ],
            }
        )

    current_conversation_key = f"conversation:{user_id}:current"
    current_conversation = redis_client.get(current_conversation_key)

    if current_conversation:
        conversation_history.append(
            {
                "conversation_id": "current",
                "messages": json.loads(current_conversation.decode("utf-8")),
            }
        )

    return jsonify({"conversations": conversation_history}), 200
