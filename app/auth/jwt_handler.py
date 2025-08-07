import time
import jwt
from decouple import config

# Load values from .env
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")

def create_access_token(user_id: int) -> str:
    """
    Create a JWT token for a user.
    :param user_id: The ID of the user.
    :return: Encoded JWT token.
    """
    payload = {
        "user_id": user_id,
        "exp": int(time.time()) + 3600  # 1-hour expiry (use int for consistency)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token.
    :param token: JWT token string.
    :return: Decoded payload or None if invalid/expired.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded  # If invalid or expired, jwt will raise an exception
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
