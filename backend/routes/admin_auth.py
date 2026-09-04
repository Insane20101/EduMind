from fastapi import APIRouter, Request, HTTPException, Depends
from database import db
from schemas import AdminLogin, AdminCredentialsUpdate
from jwt_utils import create_access_token, get_current_admin_user
from utils.security import hash_password, verify_password
from datetime import timedelta
from limiter import limiter

router = APIRouter()

@router.post("/login")
@limiter.limit("10/minute")
async def admin_login(request: Request, login_data: AdminLogin):
    admin_user = await db.admin_credentials.find_one({"admin_id": login_data.admin_id})
    if not admin_user:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
        
    if not verify_password(login_data.password, admin_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
        
    access_token_expires = timedelta(hours=2)
    access_token = create_access_token(
        data={"admin_id": login_data.admin_id},
        expires_delta=access_token_expires,
        additional_claims={"token_type": "admin"}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/credentials")
async def update_admin_credentials(
    update_data: AdminCredentialsUpdate,
    current_admin: dict = Depends(get_current_admin_user)
):
    if not verify_password(update_data.current_password, current_admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Current password incorrect")
        
    update_fields = {}
    new_admin_id = current_admin["admin_id"]
    
    if update_data.new_admin_id:
        # Check if new admin id exists (if changing to something else)
        if update_data.new_admin_id != current_admin["admin_id"]:
            existing = await db.admin_credentials.find_one({"admin_id": update_data.new_admin_id})
            if existing:
                raise HTTPException(status_code=400, detail="Admin ID already in use")
        update_fields["admin_id"] = update_data.new_admin_id
        new_admin_id = update_data.new_admin_id
        
    if update_data.new_password:
        if len(update_data.new_password) < 8:
            raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
        update_fields["password_hash"] = hash_password(update_data.new_password)
        
    if not update_fields:
        raise HTTPException(status_code=400, detail="No updates provided")
        
    await db.admin_credentials.update_one(
        {"_id": current_admin["_id"]},
        {"$set": update_fields}
    )
    
    # Issue a fresh token
    access_token_expires = timedelta(hours=2)
    access_token = create_access_token(
        data={"admin_id": new_admin_id},
        expires_delta=access_token_expires,
        additional_claims={"token_type": "admin"}
    )
    
    return {"message": "Credentials updated successfully", "access_token": access_token, "token_type": "bearer"}
