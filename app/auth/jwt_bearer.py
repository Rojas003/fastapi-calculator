from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_access_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = credentials.credentials
            payload = decode_access_token(token)
            if "error" in payload:
                raise HTTPException(status_code=401, detail=payload["error"])
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization token")
