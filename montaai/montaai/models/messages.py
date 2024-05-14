from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as EnumField
from sqlalchemy.orm import relationship
from datetime import datetime
from montaai.helpers.database import db
import enum


class MessageRole(enum.Enum):
    USER = "user"


class Message(db.Model):
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"))
    content = Column(Text)
    role = db.Column(EnumField(MessageRole), default=MessageRole.USER, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")
