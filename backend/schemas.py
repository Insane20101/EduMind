from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class UserCreate(BaseModel):
    enrollment: str
    recovery_email: str
    branch: str
    semester: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    enrollment: str
    password: str

class SendOTPRequest(BaseModel):
    enrollment: str
    recovery_email: str

class VerifyOTPResetPasswordRequest(BaseModel):
    enrollment: str
    otp_code: str
    new_password: str = Field(..., min_length=8)

class UserPasswordReset(BaseModel):
    enrollment: str
    first_name: str
    new_password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    semester: Optional[str] = None

class UserResponse(BaseModel):
    enrollment: str
    recovery_email: Optional[str] = None
    branch: str
    semester: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    created_at: datetime

class SubjectPlaylist(BaseModel):
    channel: str
    title: str
    url: str

class Subject(BaseModel):
    semester: str
    code: str
    name: str
    status: str
    playlists: List[SubjectPlaylist] = []
    note: Optional[str] = None

class AdminCredentialsBase(BaseModel):
    admin_id: str

class AdminLogin(AdminCredentialsBase):
    password: str

class AdminCredentialsUpdate(BaseModel):
    current_password: str
    new_admin_id: Optional[str] = None
    new_password: Optional[str] = None

class Resource(BaseModel):
    resource_id: str
    subject_id: str
    resource_type: str
    title: str
    file_id: Optional[str] = None
    source: Optional[str] = None
    status: str
    uploaded_by: str
    uploaded_at: datetime
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    reject_reason: Optional[str] = None
