from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
import uuid
from ..database import Base

class Component(Base):
    __tablename__ = "components"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)
    organisation_id = Column(String, ForeignKey("organisations.id"), nullable=False)

    systems = relationship("System", secondary="system_components", back_populates="components")
    dependencies = relationship("ComponentDependency", foreign_keys="[ComponentDependency.source_component_id]", back_populates="source")
    dependents = relationship("ComponentDependency", foreign_keys="[ComponentDependency.target_component_id]", back_populates="target")
    resources = relationship("Resource", secondary="component_resources", back_populates="components")
    component_apis = relationship("ComponentAPI", back_populates="component")
    organisation = relationship("Organisation", back_populates="components")
