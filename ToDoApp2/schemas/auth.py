"""
Authentication-related Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    """Schema for user registration."""
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    password: str
    role: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """Schema for user information response."""
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
