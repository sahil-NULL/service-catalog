import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4().bytes)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    organisations = relationship("Organisation", secondary="organisation_users", back_populates="users")
    groups = relationship("Group", secondary="group_users", back_populates="users")