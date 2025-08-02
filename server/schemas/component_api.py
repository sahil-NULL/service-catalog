from pydantic import BaseModel
from uuid import UUID
from enum import Enum


# 🔹 Enum for API role
class APIRole(str, Enum):
    provides = "provides"
    consumes = "consumes"


# 🔹 Shared base schema
class ComponentAPIBase(BaseModel):
    component_id: UUID
    api_id: UUID
    role: APIRole


# 🔹 Schema for inserting new links (optional)
class ComponentAPICreate(ComponentAPIBase):
    pass


# 🔹 Schema for reading from DB
class ComponentAPIOut(ComponentAPIBase):
    class Config:
        orm_mode = True
