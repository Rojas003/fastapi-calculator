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
        "exp": time.time() + 3600  # 1-hour expiry
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode a JWT token.
    :param token: JWT token string.
    :return: Decoded payload.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
