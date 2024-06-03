# models/programming_skill.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ProgrammingSkill(Base):
    __tablename__ = 'programming_skills'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(String)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="programming_skills")