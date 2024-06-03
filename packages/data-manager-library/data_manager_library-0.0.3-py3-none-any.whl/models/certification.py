# data-library/models/certificates.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    issuing_organization = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    profile_id = Column(Integer, ForeignKey('profiles.id'))

    # Define a relationship with the Profile table
    profile = relationship("Profile", back_populates="certifications")
