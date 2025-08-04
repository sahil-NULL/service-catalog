from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class ComponentResourceBase(BaseModel):
    component_id: UUID
    resource_id: UUID


# 🔹 For creating new dependencies (optional)
class ComponentResourceCreate(ComponentResourceBase):
    pass


# 🔹 For returning dependency links
class ComponentResourceOut(ComponentResourceBase):
    class Config:
        from_attributes = True
