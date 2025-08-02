from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import BLOB as UUID
import uuid
from ..database import Base

class System(Base):
    __tablename__ = "systems"
    id = Column(String, primary_key=True, default=lambda:str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)

    components = relationship("Component", secondary="system_components",back_populates="systems")
    domains = relationship("Domain", secondary="domain_systems", back_populates="systems")
    groups = relationship("Group", secondary="group_systems", back_populates="systems")
    organisation = relationship("Organisation", back_populates="systems")