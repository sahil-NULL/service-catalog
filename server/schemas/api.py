from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class APIBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


# 🔹 For API creation
class APICreate(APIBase):
    organisation_id: UUID


# 🔹 For API updates
class APIUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None  
    description: Optional[str] = None

# 🔹 For returning API data from DB
class APIOut(APIBase):
    id: UUID
    organisation_id: UUID

    class Config:
        from_attributes = True
