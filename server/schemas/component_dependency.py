from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class ComponentDependencyBase(BaseModel):
    source_component_id: UUID
    target_component_id: UUID


# 🔹 For creating new dependencies (optional)
class ComponentDependencyCreate(ComponentDependencyBase):
    pass


# 🔹 For returning dependency links
class ComponentDependencyOut(ComponentDependencyBase):
    class Config:
        orm_mode = True
