import jwt
import datetime
from fastapi import  HTTPException
import bcrypt


SECRET_KEY = "HALOBAMBANG"  # Use a strong, secret value for JWT encoding/decoding

def encode_token(username: str) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
        'sub': username
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))