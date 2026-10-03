from datetime import datetime

from pydantic import BaseModel, ConfigDict

class WorkoutCreate(BaseModel):
    title: str
    completed: bool
    user_id: int

class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    title: str
    completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)