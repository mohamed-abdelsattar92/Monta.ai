from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from montaai.helpers.database import db


class Message(db.Model):
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"))
    content = Column(Text)
    role = Column(String(80), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")
