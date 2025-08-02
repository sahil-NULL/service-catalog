from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class OrganisationBase(BaseModel):
    name: str
    description: Optional[str] = None


# 🔹 Schema for creating an organisation
class OrganisationCreate(OrganisationBase):
    pass

# 🔹 Schema for updating an organisation
class OrganisationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# 🔹 Schema for reading an organisation from DB
class OrganisationOut(OrganisationBase):
    id: UUID
    class Config:
        from_attributes = True
