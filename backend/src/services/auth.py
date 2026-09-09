import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_sso.sso.microsoft import MicrosoftSSO



JWT_SECRET = os.environ.get("JWT_SECRET", "FAILED")
FRONT_END_URL = os.environ.get("FRONT_END_URL", "FAILED")
BACK_END_URL = os.environ.get("BACK_END_URL", "FAILED")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

microsoft_sso = MicrosoftSSO(
    client_id=os.environ.get("MICROSOFT_CLIENT_ID", "FAILED"),
    client_secret=os.environ.get("MICROSOFT_CLIENT_SECRET", "FAILED"),
    redirect_uri=f"{BACK_END_URL}/auth/callback",
    tenant="consumers",
    allow_insecure_http=True # True for local docker testing, change to False in production cloud!
)

security_bearer = HTTPBearer()

# JWT UTILITIES

def create_access_token(client_id: str) -> int:
    """Generates a custom JWT securely tied to the unique Microsoft User ID."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": client_id, # The unique Client/User ID
        "exp": expire
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)) -> str:
    """Dependency that reads, decrypts, and verifies incoming JWT bearer tokens."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return client_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")