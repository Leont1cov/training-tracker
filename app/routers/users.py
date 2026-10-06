from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserCreate

router = APIRouter()

#Добавляем пользователя
@router.post("/users", response_model=UserResponse)
def create_users(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(name=user_data.name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

#Получить пользователей
@router.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#Получить конкретного пользователя
@router.get("/users/{id}", response_model=UserResponse)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

#Изменить пользователя
@router.patch("/users/{id}", response_model=UserResponse)
def update_user(user_data: UserCreate, id: int, db: Session = Depends(get_db)):
    user = db.get(User, id)
    data = user_data.model_dump(exclude_unset=True)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

#удалить пользователя
@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()