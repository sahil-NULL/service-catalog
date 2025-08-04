from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from enum import Enum

class LinkType(str, Enum):
    direct = "direct"
    indirect = "indirect"

# 🔹 Base schema
class SystemComponentBase(BaseModel):
    system_id: UUID
    component_id: UUID
    type: Optional[LinkType] = None

# 🔹 For creating links
class SystemComponentCreate(SystemComponentBase):
    pass


# 🔹 For returning links from DB
class SystemComponentOut(SystemComponentBase):
    type: LinkType
    class Config:
        from_attributes = True
