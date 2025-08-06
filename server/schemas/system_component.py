from pydantic import BaseModel
from uuid import UUID
from typing import Optional

# 🔹 Base schema
class SystemComponentBase(BaseModel):
    system_id: UUID
    component_id: UUID
    type: str = "direct"

# 🔹 For creating links
class SystemComponentCreate(SystemComponentBase):
    pass


# 🔹 For returning links from DB
class SystemComponentOut(SystemComponentBase):
    type: str
    class Config:
        from_attributes = True
