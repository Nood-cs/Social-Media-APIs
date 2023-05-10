from passlib.context import CryptContext

# tell passlib what is the default hashing algorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)