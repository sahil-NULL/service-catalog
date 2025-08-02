from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class SystemBase(BaseModel):
    name: str
    description: Optional[str] = None


# 🔹 For creating a new system
class SystemCreate(SystemBase):
    organisation_id: UUID


# 🔹 For updating a system
class SystemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# 🔹 For returning a system from DB
class SystemOut(SystemBase):
    id: UUID
    organisation_id: UUID

    class Config:
        from_attributes = True
