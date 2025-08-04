from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class GroupResourceBase(BaseModel):
    group_id: UUID
    resource_id: UUID


# 🔹 For creating links
class GroupResourceCreate(GroupResourceBase):
    pass


# 🔹 For returning links from DB
class GroupResourceOut(GroupResourceBase):
    class Config:
        from_attributes = True