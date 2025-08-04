from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class GroupApiBase(BaseModel):
    group_id: UUID
    api_id: UUID


# 🔹 For creating links
class GroupApiCreate(GroupApiBase):
    pass


# 🔹 For returning links from DB
class GroupApiOut(GroupApiBase):
    class Config:
        from_attributes = True