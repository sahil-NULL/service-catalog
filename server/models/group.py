import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship, backref
from ..database import Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(UUID, primary_key=True, default=lambda: uuid.uuid4().bytes)
    name = Column(String, nullable=False)
    parent_group_id = Column(UUID, ForeignKey("groups.id"))
    organisation_id = Column(UUID, ForeignKey("organisations.id"))

    parent_group = relationship("Group", remote_side=[id], backref=backref("subgroups", cascade="all, delete-orphan"))

    organisation = relationship("Organisation", back_populates="groups")
    users = relationship("User", secondary="group_users", back_populates="groups")
    systems = relationship("System", secondary="group_systems", back_populates="groups")
