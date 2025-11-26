"""
User-related Pydantic schemas.
"""
from pydantic import BaseModel, Field


class UserVerification(BaseModel):
    """Schema for password change verification."""
    password: str
    new_password: str = Field(min_length=6)


class PasswordChange(BaseModel):
    """Schema for password change request."""
    current_password: str
    new_password: str = Field(min_length=6)
