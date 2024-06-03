# models/resume.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="resumes")