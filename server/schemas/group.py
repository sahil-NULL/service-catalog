from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class GroupBase(BaseModel):
    name: str


# 🔹 For group creation
class GroupCreate(GroupBase):
    parent_group_id: Optional[UUID] = None
    organisation_id: UUID


# 🔹 For partial update
class GroupUpdate(BaseModel):
    name: Optional[str] = None


# 🔹 Lightweight output for normal responses
class GroupOut(GroupBase):
    id: UUID
    parent_group_id: Optional[UUID] = None
    organisation_id: UUID

    class Config:
        from_attributes = True
