from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .workout import Workout

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)

    name: Mapped[str]

    # принимаем список тренировок у пользователя
    workouts: Mapped[list["Workout"]] = relationship(
        back_populates="user"
    )