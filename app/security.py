from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return hashed_password.verify(password, hashed_password)