from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class API(Base):
    __tablename__ = "apis"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)

    component_links = relationship("ComponentAPI", back_populates="api")
    organisation = relationship("Organisation", back_populates="apis")
