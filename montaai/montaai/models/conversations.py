from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from montaai.helpers.database import db


class Conversation(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation")
