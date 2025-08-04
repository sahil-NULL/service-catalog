from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class GroupComponentBase(BaseModel):
    group_id: UUID
    component_id: UUID


# 🔹 For creating links
class GroupComponentCreate(GroupComponentBase):
    pass


# 🔹 For returning links from DB
class GroupComponentOut(GroupComponentBase):
    class Config:
        from_attributes = True