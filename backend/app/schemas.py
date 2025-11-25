from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class StudentProfile(BaseModel):
    college: Optional[str] = None
    branch: Optional[str] = None
    year: Optional[int] = None
    skills: List[str] = []
    cgpa: Optional[float] = None
    resume_url: Optional[str] = None

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    profile: Optional[StudentProfile] = None
    created_at: datetime

class JobCreate(BaseModel):
    title: str
    description: str
    company_name: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    skills_required: List[str] = []
    application_deadline: Optional[datetime] = None

class JobOut(JobCreate):
    id: str
    posted_by: str
    posted_at: datetime
    applicants: List[str] = []

class ApplicationCreate(BaseModel):
    job_id: str
    student_id: str
    resume_snapshot: Optional[str] = None

class ApplicationOut(ApplicationCreate):
    id: str
    applied_at: datetime
    status: str
