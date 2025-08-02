import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
from ..database import Base

class Organisation(Base):
    __tablename__ = "organisations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)

    users = relationship("User", secondary="organisation_users", back_populates="organisations")
    groups = relationship("Group", back_populates="organisation")
    domains = relationship("Domain", back_populates="organisation")
    resources = relationship("Resource", back_populates="organisation")
    components = relationship("Component", back_populates="organisation")
    systems = relationship("System", back_populates="organisation")
    apis = relationship("API", back_populates="organisation")
