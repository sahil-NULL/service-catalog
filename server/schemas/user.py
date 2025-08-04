from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


# 🔹 Shared base schema
class UserBase(BaseModel):
    username: str
    email: EmailStr


# 🔹 Schema for creating a user
class UserCreate(UserBase):
    password: str


# 🔹 Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# 🔹 Schema for reading a user from DB
class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True
