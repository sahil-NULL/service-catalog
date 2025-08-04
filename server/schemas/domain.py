from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class DomainBase(BaseModel):
    name: str
    description: Optional[str] = None

# 🔹 Schema for creating a domain
class DomainCreate(DomainBase):
    organisation_id: UUID
    parent_domain_id: Optional[UUID] = None

# 🔹 Schema for updating a domain
class DomainUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# 🔹 Schema for reading a domain from DB
class DomainOut(DomainBase):
    id: UUID
    organisation_id: UUID
    parent_domain_id: Optional[UUID] = None 

    class Config:
        from_attributes = True
