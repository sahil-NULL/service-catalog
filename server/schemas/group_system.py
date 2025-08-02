from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class GroupSystemBase(BaseModel):
    group_id: UUID
    system_id: UUID


# 🔹 For creating links
class GroupSystemCreate(GroupSystemBase):
    pass


# 🔹 For returning links from DB
class GroupSystemOut(GroupSystemBase):
    class Config:
        orm_mode = True