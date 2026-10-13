from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserResponse, UserCreate, UserLogin
from app.schemas.token import Token
from app.security import create_access_token
from app.services.users import post_users, get_users, get_user_by_id, patch_user, del_user, log_user

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
def read_user(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if id != user.id: #проверка, чтобы пользователь мог получить только свой профиль
        raise HTTPException(status_code=403, detail="Forbidden")

    result = get_user_by_id(id, db)
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

#вход пользователя -> эндпоинт выдачи JWT-токена
@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    result = log_user(form_data, db)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({
        "sub": str(result.id)
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }