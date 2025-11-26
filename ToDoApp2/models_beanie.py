from datetime import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field

class User(Document):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool = True
    role: str

    class Settings:
        name = "users"

class Todo(Document):
    title: str
    description: str
    priority: int
    complete: bool = False
    owner_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    class Settings:
        name = "todos2" 