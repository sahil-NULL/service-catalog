from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class GroupUserBase(BaseModel):
    group_id: UUID
    user_id: UUID


# 🔹 For creating links
class GroupUserCreate(GroupUserBase):
    pass


# 🔹 For returning links from DB
class GroupUserOut(GroupUserBase):
    class Config:
        orm_mode = True