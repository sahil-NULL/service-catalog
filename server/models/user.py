import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)

    organisations = relationship("Organisation", secondary="organisation_users", back_populates="users")
    groups = relationship("Group", secondary="group_users", back_populates="users")
