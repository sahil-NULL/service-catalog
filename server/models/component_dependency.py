from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
from ..database import Base

class ComponentDependency(Base):
    __tablename__ = "component_dependencies"
    source_component_id = Column(UUID, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
    target_component_id = Column(UUID, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)

    source = relationship("Component", foreign_keys=[source_component_id], back_populates="dependencies")
    target = relationship("Component", foreign_keys=[target_component_id], back_populates="dependents")
