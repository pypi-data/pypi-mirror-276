# models/tech_stack.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TechStack(Base):
    __tablename__ = 'tech_stacks'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="tech_stacks")
