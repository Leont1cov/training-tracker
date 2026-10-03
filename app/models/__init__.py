from .base import Base
from .user import User
from .workout import Workout
from .exercise import Exercise
from .workout_exercise import WorkoutExercise

__all__ = [
    "Base",
    "User",
    "Workout",
    "Exercise",
    "WorkoutExercise",
]

#TODO: Добавь relationship() и back_populates