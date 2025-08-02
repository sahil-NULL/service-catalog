from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class Resource(Base):
    __tablename__ = "resources"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)

    components = relationship("Component", secondary="component_resources", back_populates="resources")
    organisation = relationship("Organisation", back_populates="resources")
