from datetime import datetime, timedelta, timezone
from app.config import settings
import jwt
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)

#создаёт защитный токен
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15) #создаёт лимит
    to_encode.update({"exp": expire}) #добавляем exp (лимит) в словарь
    return jwt.encode( #превращает подготовленные данные в подписанный JWT
        to_encode,
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM
    )