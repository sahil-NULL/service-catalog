import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship, backref
from ..database import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    parent_group_id = Column(String, ForeignKey("groups.id"))
    organisation_id = Column(String, ForeignKey("organisations.id"))

    parent_group = relationship("Group", remote_side=[id], backref=backref("subgroups", cascade="all, delete-orphan"))

    organisation = relationship("Organisation", back_populates="groups")
    users = relationship("User", secondary="group_users", back_populates="groups")
    systems = relationship("System", secondary="group_systems", back_populates="groups")
