import re
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pymongo.errors import DuplicateKeyError
from schemas import UserCreate, UserLogin, UserUpdate, UserResponse
from database import db
from jwt_utils import create_access_token, get_current_user
from utils.security import hash_password, verify_password

router = APIRouter()
ENROLL_REGEX = re.compile(r"^[A-Z0-9]{6,20}$", re.IGNORECASE)
limiter = Limiter(key_func=get_remote_address)

def validate_enrollment(enr: str, branch: str):
    clean_enr = (enr or "").strip()
    if not clean_enr or not ENROLL_REGEX.match(clean_enr):
        raise HTTPException(status_code=400, detail="Invalid enrollment format. Must be 6-20 alphanumeric characters.")
    return True

@router.post("/signup")
async def signup(user: UserCreate):
    validate_enrollment(user.enrollment, user.branch)
    
    clean_enr = user.enrollment.strip().upper()
    
    # Check if enrollment already exists (case-insensitive)
    existing = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if existing:
        raise HTTPException(status_code=400, detail="Enrollment number already registered")

    user_dict = user.dict(exclude={"password"})
    user_dict["enrollment"] = clean_enr
    user_dict["branch"] = user_dict.get("branch", "CSE").upper()
    user_dict["password_hash"] = hash_password(user.password)
    user_dict["created_at"] = datetime.utcnow()
    
    try:
        await db.users.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Enrollment number already registered")
    
    user_dict.pop("password_hash", None)
    user_dict.pop("_id", None)
    
    token = create_access_token({"enrollment": user_dict["enrollment"]})
    return {"access_token": token, "user": user_dict}

@router.post("/login")
@limiter.limit("10/minute")  # 10 login attempts per minute per IP
async def login(request: Request, credentials: UserLogin):
    clean_enr = (credentials.enrollment or "").strip().upper()
    if not clean_enr:
        raise HTTPException(status_code=400, detail="Enrollment number required.")

    user = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if not user or "password_hash" not in user or not verify_password(credentials.password.strip(), user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid enrollment number or password")
    
    user_dict = {
        "enrollment": user["enrollment"],
        "branch": user.get("branch", "CSE"),
        "semester": user.get("semester", 4),
        "first_name": user.get("first_name", "Student"),
        "middle_name": user.get("middle_name"),
        "last_name": user.get("last_name", ""),
        "created_at": user.get("created_at")
    }
    
    token = create_access_token({"enrollment": user["enrollment"]})
    return {"access_token": token, "user": user_dict}


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "enrollment": current_user["enrollment"],
        "branch": current_user["branch"],
        "semester": current_user["semester"],
        "first_name": current_user["first_name"],
        "middle_name": current_user.get("middle_name"),
        "last_name": current_user["last_name"],
        "created_at": current_user["created_at"]
    }

@router.put("/profile", response_model=UserResponse)
async def update_profile(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    await db.users.update_one({"enrollment": current_user["enrollment"]}, {"$set": update_data})
    
    # Fetch updated user
    updated_user = await db.users.find_one({"enrollment": current_user["enrollment"]})
    
    return {
        "enrollment": updated_user["enrollment"],
        "branch": updated_user["branch"],
        "semester": updated_user["semester"],
        "first_name": updated_user["first_name"],
        "middle_name": updated_user.get("middle_name"),
        "last_name": updated_user["last_name"],
        "created_at": updated_user["created_at"]
    }
