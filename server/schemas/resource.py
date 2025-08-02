from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Base schema (shared fields)
class ResourceBase(BaseModel):
    name: str
    type: str 
    description: Optional[str] = None


# 🔹 For resource creation
class ResourceCreate(ResourceBase):
    organisation_id: UUID


# 🔹 For resource update
class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

# 🔹 For DB reads / API responses
class ResourceOut(ResourceBase):
    id: UUID
    organisation_id: UUID

    class Config:
        from_attributes = True
