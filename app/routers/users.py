from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserResponse, UserCreate
from app.services.users import post_users, get_users, get_user_by_id, patch_user, del_user

router = APIRouter()

#Добавляем пользователя
@router.post("/users", response_model=UserResponse)
def create_users(user_data: UserCreate, db: Session = Depends(get_db)):
    return post_users(user_data, db)

#Получить пользователей
@router.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

#Получить конкретного пользователя
@router.get("/users/{id}", response_model=UserResponse)
def read_user(id: int, db: Session = Depends(get_db)):
    result = get_user_by_id(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

#Изменить пользователя
@router.patch("/users/{id}", response_model=UserResponse)
def update_user(user_data: UserCreate, id: int, db: Session = Depends(get_db)):
    result = patch_user(user_data, id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

#удалить пользователя
@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    result = del_user(id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result