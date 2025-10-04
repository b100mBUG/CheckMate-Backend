from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


def hash_pwd(password):
    return pwd_context.hash(password)

def is_verified_pwd(inputted_pwd, hashed_pwd):
    return pwd_context.verify(hashed_pwd, inputted_pwd)

def current_date():
    today = datetime.today().date()
    return today
