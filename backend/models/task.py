from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime, timezone
import uuid

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: Literal["High", "Medium", "Low"] = "Medium"
    due_date: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Literal["High", "Medium", "Low"]] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    due_date: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    created_at: str
    updated_at: str

class TaskInDB(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "Medium"
    due_date: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    high_priority: int
    medium_priority: int
    low_priority: int
    overdue: int
    due_today: int
    categories: dict
