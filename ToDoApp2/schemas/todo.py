"""
Todo-related Pydantic schemas.
"""
from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    """Schema for creating/updating a todo."""
    title: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool = False


class TodoResponse(BaseModel):
    """Schema for todo response."""
    id: str
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: str
