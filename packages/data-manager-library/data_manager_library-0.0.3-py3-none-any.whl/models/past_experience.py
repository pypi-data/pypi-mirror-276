# models/past_experience.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class PastExperience(Base):
    __tablename__ = 'past_experiences'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String)
    description = Column(Text)
    start_date = Column(String)
    end_date = Column(String, nullable=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="past_experiences")