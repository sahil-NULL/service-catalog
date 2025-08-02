from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class SystemComponentBase(BaseModel):
    system_id: UUID
    component_id: UUID


# 🔹 For creating links
class SystemComponentCreate(SystemComponentBase):
    pass


# 🔹 For returning links from DB
class SystemComponentOut(SystemComponentBase):
    class Config:
        orm_mode = True