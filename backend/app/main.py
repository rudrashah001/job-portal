from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize App
app = FastAPI()

# include routers
from app.routes import jobs as jobs_router
from app.routes import students as students_router
from app.routes import recruiters as recruiters_router
from app.routes import admin as admin_router

app.include_router(jobs_router.router, prefix="/jobs")
app.include_router(students_router.router, prefix="/students")
app.include_router(recruiters_router.router, prefix="/recruiters")
app.include_router(admin_router.router, prefix="/admin")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["AuthDB"]
users = db["users"]

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility Functions

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@app.post("/register")
def register_user(user: User):
    if users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    users.insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User registered successfully"}

@app.post("/login", response_model=Token)
def login(user: User):
    db_user = users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", include_in_schema=False)
def home(request: Request):
    """If the caller is a browser (accepts html) redirect to the docs,
    otherwise return a small JSON health response.
    """
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return RedirectResponse(url="/docs")
    return {"message": "FastAPI Authentication System Running"}
