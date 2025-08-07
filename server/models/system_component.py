from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class SystemComponent(Base):
    __tablename__ = "system_components"
    system_id = Column(String, ForeignKey("systems.id", ondelete="CASCADE"), primary_key=True)
    component_id = Column(String, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
    type = Column(String, nullable=False, default="direct")

    system = relationship("System", back_populates="system_components")
    component = relationship("Component", back_populates="component_links")
