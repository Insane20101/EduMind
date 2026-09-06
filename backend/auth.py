import re
import random
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

from schemas import (

    UserCreate, UserLogin, UserUpdate, UserResponse, 
    UserPasswordReset, SendOTPRequest, SendSignupOTPRequest, VerifyOTPResetPasswordRequest
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
        return "your recovery email"
    parts = email.split("@")
    name = parts[0]
    domain = parts[1]
    if len(name) <= 2:
        masked_name = name[0] + "*"
    else:
        masked_name = name[0] + "*" * (len(name) - 2) + name[-1]
    return f"{masked_name}@{domain}"

@router.post("/send-signup-otp")
@limiter.limit("5/minute")
async def send_signup_otp(request: Request, payload: SendSignupOTPRequest):
    clean_enr = (payload.enrollment or "").strip().upper()
    clean_rec_email = (payload.recovery_email or "").strip().lower()
    first_name = (payload.first_name or "Student").strip()

    if not clean_enr or not clean_rec_email:
        raise HTTPException(status_code=400, detail="Both Enrollment Number and Recovery Email ID are required.")
    
    if not EMAIL_REGEX.match(clean_rec_email):
        raise HTTPException(status_code=400, detail="Valid Recovery Email ID is required.")

    validate_enrollment(clean_enr, "CSE")

    # Early check 1: Enrollment already exists?
    existing_enr = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if existing_enr:
        raise HTTPException(status_code=400, detail="Enrollment number already registered.")

    # Early check 2: Email already registered?
    existing_email = await db.users.find_one({
        "$or": [
            {"recovery_email": {"$regex": f"^{re.escape(clean_rec_email)}$", "$options": "i"}},
            {"email": {"$regex": f"^{re.escape(clean_rec_email)}$", "$options": "i"}}
        ]
    })
    if existing_email:
        raise HTTPException(status_code=400, detail="Email address already registered.")

    # Generate 6-digit OTP code
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Upsert OTP record for signup
    await db.signup_otps.update_one(
        {"recovery_email": clean_rec_email},
        {"$set": {
            "enrollment": clean_enr,
            "recovery_email": clean_rec_email,
            "otp_code": otp_code,
            "attempts": 0,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )

    email_sent = send_resend_otp_email(clean_rec_email, first_name, otp_code, context="signup")
    masked = mask_email(clean_rec_email)

    if not email_sent:
        logger.warning(f"[SIGNUP OTP GENERATED] OTP code for {clean_rec_email}: {otp_code}")

    msg = f"6-digit verification code sent to {masked}" if email_sent else f"Verification code generated for {masked}. (Email delivery note: check Resend API key & domain configuration)."

    return {
        "message": msg,
        "masked_email": masked,
        "email_sent": email_sent
    }



@router.post("/signup")
async def signup(user: UserCreate):
    validate_enrollment(user.enrollment, user.branch)
    
    clean_enr = user.enrollment.strip().upper()
    clean_rec_email = (user.recovery_email or "").strip().lower()
    submitted_otp = (user.otp_code or "").strip()

    if not clean_rec_email or not EMAIL_REGEX.match(clean_rec_email):
        raise HTTPException(status_code=400, detail="Valid Recovery Email ID is required.")
    
    if not submitted_otp or len(submitted_otp) != 6:
        raise HTTPException(status_code=400, detail="6-digit verification code is required.")

    # Verify pending OTP
    otp_record = await db.signup_otps.find_one({"recovery_email": clean_rec_email})
    if not otp_record:
        raise HTTPException(status_code=400, detail="No pending verification code found for this email. Please click 'Resend Code'.")

    if otp_record.get("expires_at") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new code.")

    if otp_record.get("attempts", 0) >= 5:
        raise HTTPException(status_code=400, detail="Too many failed verification attempts. Please request a new verification code.")

    if otp_record.get("otp_code") != submitted_otp:
        await db.signup_otps.update_one(
            {"recovery_email": clean_rec_email},
            {"$inc": {"attempts": 1}}
        )
        raise HTTPException(status_code=400, detail="Invalid verification code. Please check your email.")

    # Check enrollment existence
    existing_enr = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if existing_enr:
        raise HTTPException(status_code=400, detail="Enrollment number already registered.")

    # Check email existence
    existing_email = await db.users.find_one({
        "$or": [
            {"recovery_email": {"$regex": f"^{re.escape(clean_rec_email)}$", "$options": "i"}},
            {"email": {"$regex": f"^{re.escape(clean_rec_email)}$", "$options": "i"}}
        ]
    })
    if existing_email:
        raise HTTPException(status_code=400, detail="Email address already registered.")

    user_dict = user.dict(exclude={"password", "otp_code"})
    user_dict["enrollment"] = clean_enr
    user_dict["recovery_email"] = clean_rec_email
    user_dict["branch"] = user_dict.get("branch", "CSE").upper()
    user_dict["password_hash"] = hash_password(user.password.strip())
    user_dict["created_at"] = datetime.utcnow()
    
    try:
        await db.users.insert_one(user_dict)
    except DuplicateKeyError as e:
        err_msg = str(e)
        if "Email" in err_msg or "recovery_email" in err_msg:
            raise HTTPException(status_code=400, detail="Email address already registered.")
        raise HTTPException(status_code=400, detail="Enrollment number already registered.")
    
    # Clean up OTP record on success
    await db.signup_otps.delete_one({"recovery_email": clean_rec_email})

    user_dict.pop("password_hash", None)
    user_dict.pop("_id", None)
    
    token = create_access_token({"enrollment": user_dict["enrollment"]})
    return {"access_token": token, "user": user_dict}


@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, credentials: UserLogin):
    clean_enr = (credentials.enrollment or "").strip().upper()
    if not clean_enr:
        raise HTTPException(status_code=400, detail="Enrollment number required.")

    # Primary login strictly by Enrollment Number
    user = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    
    if not user or "password_hash" not in user:
        # Check if user is attempting to log in as admin on student login endpoint
        admin = await db.admin_credentials.find_one({"admin_id": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
        if admin:
            raise HTTPException(status_code=400, detail="This is an Admin account. Please use the Admin Login portal at /admin/login.")
        raise HTTPException(status_code=401, detail="Invalid enrollment number or password.")

    raw_pw = credentials.password or ""
    clean_pw = raw_pw.strip()

    is_valid = verify_password(clean_pw, user["password_hash"]) or verify_password(raw_pw, user["password_hash"])
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid enrollment number or password.")
    
    user_dict = {
        "enrollment": user["enrollment"],
        "recovery_email": user.get("recovery_email") or user.get("email"),
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
    clean_rec_email = (payload.recovery_email or "").strip().lower()

    if not clean_enr or not clean_rec_email:
        raise HTTPException(status_code=400, detail="Both Enrollment Number and Recovery Email ID are required.")

    user = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})

    if not user:
        raise HTTPException(status_code=404, detail="Enrollment number not registered. Please check or sign up.")

    registered_rec_email = (user.get("recovery_email") or user.get("email") or "").strip().lower()
    if not registered_rec_email:
        raise HTTPException(status_code=400, detail="No registered recovery email found for this enrollment. Please contact admin.")

    # Strict Security Check: Verify submitted recovery email matches registered recovery email
    if registered_rec_email != clean_rec_email:
        raise HTTPException(status_code=400, detail="Recovery Email ID does not match the registered record for this Enrollment Number.")

    # Generate 6-digit OTP
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    # Upsert OTP into otps collection
    await db.otps.update_one(
        {"enrollment": user["enrollment"]},
        {"$set": {
            "enrollment": user["enrollment"],
            "recovery_email": registered_rec_email,
            "otp_code": otp_code,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )

    student_name = user.get("first_name", "Student")
    email_sent = send_resend_otp_email(registered_rec_email, student_name, otp_code, context="password_reset")
    masked = mask_email(registered_rec_email)

    if not email_sent:
        logger.warning(f"[RESET OTP GENERATED] OTP code for {registered_rec_email}: {otp_code}")

    msg = f"6-digit verification code sent to {masked}" if email_sent else f"Verification code generated for {masked}. (Email delivery note: check Resend API key & domain configuration)."

    return {
        "message": msg,
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

    user = await db.users.find_one({"enrollment": {"$regex": f"^{re.escape(clean_enr)}$", "$options": "i"}})
    if not user:
        raise HTTPException(status_code=404, detail="Account not found.")

    otp_record = await db.otps.find_one({"enrollment": user["enrollment"]})
    if not otp_record or otp_record.get("otp_code") != clean_otp:
        raise HTTPException(status_code=400, detail="Invalid 6-digit verification code. Please check your email.")

    if otp_record.get("expires_at") < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired. Please click 'Resend Code'.")

    # Update password hash
    new_hash = hash_password(new_pw)
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"password_hash": new_hash}}
    )

    # Delete used OTP
    await db.otps.delete_one({"_id": otp_record["_id"]})

    return {"message": "Password reset successfully! You can now log in with your Enrollment Number and new password."}

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "enrollment": current_user["enrollment"],
        "recovery_email": current_user.get("recovery_email") or current_user.get("email"),
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
        "recovery_email": updated_user.get("recovery_email") or updated_user.get("email"),
        "branch": updated_user["branch"],
        "semester": updated_user["semester"],
        "first_name": updated_user["first_name"],
        "middle_name": updated_user.get("middle_name"),
        "last_name": updated_user["last_name"],
        "created_at": updated_user["created_at"]
    }
