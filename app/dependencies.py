from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") #создаёт объект, который извлекает токен из HTTP-заголовка

#Аутентификация - подтверждаем, что токен принадлежит пользователю
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_access_token(token) #проверяет токен и извлекает id пользователя
    user = db.get(User, user_id)
    if not user: #если не найден, ошибка 401
        raise HTTPException(status_code=401, detail="User not found")
    return user #если пользователь найден, возвращаем его объект