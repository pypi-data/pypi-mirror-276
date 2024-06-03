# data-library/models/contact_request.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class ContactRequest(Base):
    __tablename__ = 'contact_requests'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: If you want to establish a relationship with the Profile table
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profile = relationship("Profile", back_populates="contact_requests")
