import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
from ..database import Base

class Domain(Base):
    __tablename__ = "domains"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)

    organisation = relationship("Organisation", back_populates="domains")
    systems = relationship("System", secondary="domain_systems", back_populates="domains")