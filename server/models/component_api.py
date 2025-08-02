from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import relationship
from ..database import Base

class ComponentAPI(Base):
    __tablename__ = "component_apis"
    component_id = Column(UUID, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
    api_id = Column(UUID, ForeignKey("apis.id", ondelete="CASCADE"), primary_key=True)
    role = Column(Enum("provides", "consumes", name="api_role_enum"))

    component = relationship("Component", back_populates="component_apis")
    api = relationship("API", back_populates="component_links")
