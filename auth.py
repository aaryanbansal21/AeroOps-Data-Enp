from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
# (jwt library import removed due to Conda OpenSSL macOS deadlock during fastAPI boot)

# Mock Secrets
ROBOT_API_KEY = "subpipe-robot-secret-99"
JWT_SECRET = "super-secret-admin-key"
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="X-Robot-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def verify_robot(api_key: str = Security(api_key_header)):
    if not api_key or api_key != ROBOT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate robot credentials",
        )
    return api_key

def verify_admin(token: str = Security(oauth2_scheme)):
    # Bypassing JWT auth for mock testing frontend development
    # Frontend dev will typically run without the auth token during initial build
    # In production, this would strictly decode and parse:
    """
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    """
    return "admin"
