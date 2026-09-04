import re
import random
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pymongo.errors import DuplicateKeyError

from schemas import (
    UserCreate, UserLogin, UserUpdate, UserResponse, 
    UserPasswordReset, SendOTPRequest, VerifyOTPResetPasswordRequest
)
from database import db
from jwt_utils import create_access_token, get_current_user
from utils.security import hash_password, verify_password
from utils.email_utils import send_resend_otp_email

router = APIRouter()
ENROLL_REGEX = re.compile(r"^[A-Z0-9]{6,20}$", re.IGNORECASE)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
limiter = Limiter(key_func=get_remote_address)

def validate_enrollment(enr: str, branch: str):
    clean_enr = (enr or "").strip()
    if not clean_enr or not ENROLL_REGEX.match(clean_enr):
        raise HTTPException(status_code=400, detail="Invalid enrollment format. Must be 6-20 alphanumeric characters.")
    return True

def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return "your registered email"
    parts = email.split("@")
    name = parts[0]
    domain = parts[1]
    if len(name) <= 2:
        masked_name = name[0] + "*"
    else:
        masked_name = name[0] + "*" * (len(name) - 2) + name[-1]
    return f"{masked_name}@{domain}"

@router.post("/signup")
async def signup(user: UserCreate):
    validate_enrollment(user.enrollment, user.branch)
    
    clean_enr = user.enrollment.strip().upper()
    clean_email = (user.email or "").strip().lower() if user.email else None

    if clean_email and not EMAIL_REGEX.match(clean_email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    
    # Check if enrollment already exists
    existing_enr = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if existing_enr:
        raise HTTPException(status_code=400, detail="Enrollment number already registered.")

    # Check if email already exists
    if clean_email:
        existing_email = await db.users.find_one({"email": clean_email})
        if existing_email:
            raise HTTPException(status_code=400, detail="Email address already registered.")

    user_dict = user.dict(exclude={"password"})
    user_dict["enrollment"] = clean_enr
    user_dict["email"] = clean_email
    user_dict["branch"] = user_dict.get("branch", "CSE").upper()
    user_dict["password_hash"] = hash_password(user.password.strip())
    user_dict["created_at"] = datetime.utcnow()
    
    try:
        await db.users.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Enrollment number or email already registered.")
    
    user_dict.pop("password_hash", None)
    user_dict.pop("_id", None)
    
    token = create_access_token({"enrollment": user_dict["enrollment"]})
    return {"access_token": token, "user": user_dict}

@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin):
    clean_identifier = (credentials.enrollment or "").strip()
    if not clean_identifier:
        raise HTTPException(status_code=400, detail="Enrollment number or Email required.")

    # Support login by enrollment OR email
    user = await db.users.find_one({
        "$or": [
            {"enrollment": {"$regex": f"^{re.escape(clean_identifier.upper())}$", "$options": "i"}},
            {"email": clean_identifier.lower()}
        ]
    })
    
    if not user or "password_hash" not in user:
        raise HTTPException(status_code=401, detail="Invalid credentials or password.")

    raw_pw = credentials.password or ""
    clean_pw = raw_pw.strip()

    is_valid = verify_password(clean_pw, user["password_hash"]) or verify_password(raw_pw, user["password_hash"])
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials or password.")
    
    user_dict = {
        "enrollment": user["enrollment"],
        "email": user.get("email"),
        "branch": user.get("branch", "CSE"),
        "semester": user.get("semester", 4),
        "first_name": user.get("first_name", "Student"),
        "middle_name": user.get("middle_name"),
        "last_name": user.get("last_name", ""),
        "created_at": user.get("created_at")
    }
    
    token = create_access_token({"enrollment": user["enrollment"]})
    return {"access_token": token, "user": user_dict}

@router.post("/send-otp")
@limiter.limit("5/minute")
async def send_otp(request: Request, payload: SendOTPRequest):
    clean_enr = (payload.enrollment or "").strip().upper()
    if not clean_enr:
        raise HTTPException(status_code=400, detail="Enrollment number required.")

    user = await db.users.find_one({
        "$or": [
            {"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}},
            {"email": clean_enr.lower()}
        ]
    })

    if not user:
        raise HTTPException(status_code=404, detail="Enrollment number or email not registered.")

    student_email = user.get("email")
    if not student_email:
        raise HTTPException(status_code=400, detail="No registered email address found for this account. Please contact admin to reset.")

    # Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Upsert OTP into collection
    await db.otps.update_one(
        {"enrollment": user["enrollment"]},
        {"$set": {
            "enrollment": user["enrollment"],
            "email": student_email,
            "otp_code": otp_code,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )

    student_name = user.get("first_name", "Student")
    email_sent = send_resend_otp_email(student_email, student_name, otp_code)

    masked = mask_email(student_email)
    return {
        "message": f"6-digit verification code sent to {masked}",
        "masked_email": masked,
        "email_sent": email_sent
    }

@router.post("/verify-otp-reset-password")
@limiter.limit("5/minute")
async def verify_otp_reset_password(request: Request, payload: VerifyOTPResetPasswordRequest):
    clean_enr = (payload.enrollment or "").strip().upper()
    clean_otp = (payload.otp_code or "").strip()
    new_pw = (payload.new_password or "").strip()

    if not clean_enr or not clean_otp or not new_pw:
        raise HTTPException(status_code=400, detail="All fields (enrollment, verification code, new password) are required.")

    if len(new_pw) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters long.")

    user = await db.users.find_one({
        "$or": [
            {"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}},
            {"email": clean_enr.lower()}
        ]
    })
    if not user:
        raise HTTPException(status_code=404, detail="Account not found.")

    otp_record = await db.otps.find_one({"enrollment": user["enrollment"]})
    if not otp_record or otp_record.get("otp_code") != clean_otp:
        raise HTTPException(status_code=400, detail="Invalid 6-digit verification code. Please check your email.")

    if otp_record.get("expires_at") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired. Please click 'Resend Code'.")

    # Update password
    new_hash = hash_password(new_pw)
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": new_hash}}
    )

    # Delete used OTP
    await db.otps.delete_one({"_id": otp_record["_id"]})

    return {"message": "Password reset successfully! You can now log in with your new password."}

@router.post("/reset-password")
@limiter.limit("5/minute")
async def reset_password(request: Request, data: UserPasswordReset):
    """Fallback reset endpoint matching first_name verification."""
    clean_enr = (data.enrollment or "").strip().upper()
    clean_name = (data.first_name or "").strip()
    new_pw = (data.new_password or "").strip()

    if not clean_enr or not clean_name or not new_pw:
        raise HTTPException(status_code=400, detail="All fields are required.")

    if len(new_pw) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters long.")

    user = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail="Enrollment number not found.")

    user_first_name = (user.get("first_name") or "").strip()
    if user_first_name.lower() != clean_name.lower():
        raise HTTPException(status_code=400, detail="First name does not match the registered record.")

    new_hash = hash_password(new_pw)
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": new_hash}}
    )

    return {"message": "Password reset successfully! You can now log in with your new password."}

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "enrollment": current_user["enrollment"],
        "email": current_user.get("email"),
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
    updated_user = await db.users.find_one({"enrollment": current_user["enrollment"]})
    
    return {
        "enrollment": updated_user["enrollment"],
        "email": updated_user.get("email"),
        "branch": updated_user["branch"],
        "semester": updated_user["semester"],
        "first_name": updated_user["first_name"],
        "middle_name": updated_user.get("middle_name"),
        "last_name": updated_user["last_name"],
        "created_at": updated_user["created_at"]
    }
