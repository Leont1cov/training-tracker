from datetime import datetime

from sqlalchemy import Identity, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .workout_exercise import WorkoutExercise

class Workout(Base):
    __tablename__ = 'workouts'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str]
    completed: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    user: Mapped["User"] = relationship(back_populates="workouts")
    workout_exercises: Mapped[list["WorkoutExercise"]] = relationship(
        back_populates="workout"
    )