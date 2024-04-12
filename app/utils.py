# This is just to save anything releated with hashing password in one place to make our
# main.py more clearner

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str): #This function hashes password for us
    return pwd_context.hash(password)

def verify(plain_password, hashed_password): #this function hash the pwd user supply while trying to login, and compare with the one on db
    return pwd_context.verify(plain_password, hashed_password)
