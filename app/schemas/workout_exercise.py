from pydantic import BaseModel, ConfigDict

class WorkoutExerciseCreate(BaseModel):
    workout_id: int
    exercise_id: int
    sets: int
    reps: int
    weight: float

class WorkoutExerciseResponse(BaseModel):
    id: int
    workout_id: int
    exercise_id: int
    sets: int
    reps: int
    weight: float
    model_config = ConfigDict(from_attributes=True)