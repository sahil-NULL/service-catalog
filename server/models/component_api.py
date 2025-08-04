from sqlalchemy import Column, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from ..database import Base

class ComponentAPI(Base):
    __tablename__ = "component_apis"
    component_id = Column(String, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True)
    api_id = Column(String, ForeignKey("apis.id", ondelete="CASCADE"), primary_key=True)
    role = Column(Enum("provides", "consumes", name="api_role_enum"), nullable=False)

    component = relationship("Component", back_populates="component_apis")
    api = relationship("API", back_populates="component_links")
