from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False
    is_authenticated: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """Properties to receive via API on update."""


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """Additional properties to return via API."""
