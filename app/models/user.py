from sqlalchemy import Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING: #убираем возможную цикличность импортов с помощью Type_Checking
    # Этот импорт нужен PyCharm/анализатору типов, но не выполняй его при обычном запуске программы.
    from .workout import Workout

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)

    name: Mapped[str]

    password_hash: Mapped[str]

    # принимаем список тренировок у пользователя
    workouts: Mapped[list["Workout"]] = relationship(
        back_populates="user"
    )