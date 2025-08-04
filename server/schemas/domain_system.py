from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class DomainSystemBase(BaseModel):
    domain_id: UUID
    system_id: UUID


# 🔹 For creating links
class DomainSystemCreate(DomainSystemBase):
    pass


# 🔹 For returning links from DB
class DomainSystemOut(DomainSystemBase):
    class Config:
        from_attributes = True