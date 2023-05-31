from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(user_password: str, hashed_password: str):
    return pwd_context.verify(user_password, hashed_password)

