# models/profile.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    projects = relationship('Project', back_populates='profile')
    certifications = relationship('Certification', back_populates='profile')
    contacts = relationship('Contact', back_populates='profile')
    past_experiences = relationship('PastExperience', back_populates='profile')
    programming_skills = relationship('ProgrammingSkill', back_populates='profile')
    resumes = relationship('Resume', back_populates='profile')
    soft_skills = relationship('SoftSkill', back_populates='profile')
    tech_stacks = relationship('TechStack', back_populates='profile')
    contact_requests = relationship('ContactRequest', back_populates='profile')