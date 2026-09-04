import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import db

SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None, additional_claims: dict = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    if additional_claims:
        to_encode.update(additional_claims)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_current_user(payload: dict = Security(verify_token)):
    # Standard user check - ensure it's not an admin token by checking token_type
    if payload.get("token_type") == "admin":
        raise HTTPException(status_code=401, detail="Invalid token type")
        
    enrollment = payload.get("enrollment")
    if not enrollment:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db.users.find_one({"enrollment": enrollment})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_admin_user(payload: dict = Security(verify_token)):
    if payload.get("token_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required.")

        
    admin_id = payload.get("admin_id")
    if not admin_id:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    admin_user = await db.admin_credentials.find_one({"admin_id": admin_id})
    if not admin_user:
        admin_user = {"admin_id": admin_id}
        
    return admin_user

