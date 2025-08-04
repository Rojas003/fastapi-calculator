import jwt
from fastapi import HTTPException
from datetime import datetime
from app.core.config import settings

def decode_access_token(token: str):
    """
    Decode a JWT token and return its payload if valid.
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("exp") and datetime.utcnow().timestamp() > payload["exp"]:
            return None
        return payload
    except jwt.PyJWTError:
        return None
