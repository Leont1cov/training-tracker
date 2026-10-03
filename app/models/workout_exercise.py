from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .workout import Workout
from .exercise import Exercise

class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey('workouts.id'), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercises.id'), nullable=False)

    sets: Mapped[int]
    reps: Mapped[int]
    weight: Mapped[float]

    workout: Mapped["Workout"] = relationship(
        back_populates="workout_exercises"
    )

    exercise: Mapped["Exercise"] = relationship(
        back_populates="workout_exercises"
    )