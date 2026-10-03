from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .workout_exercise import WorkoutExercise

class Exercise(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)

    title: Mapped[str]

    workout_exercises: Mapped[list["WorkoutExercise"]] = relationship(back_populates="exercise")