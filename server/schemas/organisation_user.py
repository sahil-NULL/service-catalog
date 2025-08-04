from pydantic import BaseModel
from uuid import UUID


# 🔹 Base schema
class OrganisationUserBase(BaseModel):
    organisation_id: UUID
    user_id: UUID


# 🔹 For creating links
class OrganisationUserCreate(OrganisationUserBase):
    pass


# 🔹 For returning links from DB
class OrganisationUserOut(OrganisationUserBase):
    class Config:
        from_attributes = True
