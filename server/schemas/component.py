from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# Basic component schema — used in normal API responses
class ComponentBase(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


# Component response (from DB)
class ComponentOut(ComponentBase):
    id: UUID
    organisation_id: UUID

    class Config:
        from_attributes = True


# Schema for creating a new component
class ComponentCreate(ComponentBase):
    organisation_id: UUID


# Schema for updating a component
class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
