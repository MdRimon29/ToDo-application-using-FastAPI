from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
# from pwdlib.hashers.bcrypt import BcryptHasher
# from passlib.context import CryptContext

password_hash = PasswordHash(hashers=[Argon2Hasher()])
# password_hash = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)