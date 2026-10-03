from pydantic import BaseModel, ConfigDict

class ExerciseCreate(BaseModel):
    title: str

class ExerciseResponse(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)