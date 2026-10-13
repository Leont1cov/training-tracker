from app.models import User
from app.security import hash_password, verify_password


def post_users(user_data, db):
    hashed_password = hash_password(user_data.password)

    user = User(name=user_data.name, password_hash=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_users(db):
    return db.query(User).all()

def get_user_by_id(id, db):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    return user

def patch_user(user_data, id, db):
    user = db.get(User, id)
    data = user_data.model_dump(exclude_unset=True)

    if not user:
        return None

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

def del_user(id, db):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return True

def log_user(user_data, db):
    user = db.query(User).filter(User.name == user_data.username).first()
    if not user:
        return None

    if not verify_password(user_data.password, user.password_hash):
        return None
    return user