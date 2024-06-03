# models/contact.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    phone = Column(String)
    address = Column(String)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="contacts")