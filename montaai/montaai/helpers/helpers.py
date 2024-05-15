import json

from montaai.helpers.database import redis_client, db
from montaai.models.conversations import Conversation
from montaai.models.messages import Message
from montaai.models.users import User


new_messages_keeper = []


def save_current_conversation_to_db(conversation_id, messages_to_save, user_id):
    existing_conversation: Conversation = Conversation.query.filter_by(
        id=conversation_id
    ).first()

    if existing_conversation:
        for message in messages_to_save:
            new_db_message = Message(
                conversation_id=existing_conversation.id,
                role=message["role"],
                content=message["content"],
            )
            db.session.add(new_db_message)
    else:
        new_db_conversation_for_current_conversation = Conversation(user_id=user_id)
        db.session.add(new_db_conversation_for_current_conversation)

        for message in messages_to_save:
            new_db_message = Message(
                conversation_id=new_db_conversation_for_current_conversation.id,
                role=message["role"],
                content=message["content"],
            )
            db.session.add(new_db_message)
    db.session.commit()
    new_messages_keeper.clear()
