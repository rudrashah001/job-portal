import sys
import traceback

print("Step-by-step import of students.py dependencies...")

try:
    print("\n1. Import FastAPI APIRouter...")
    from fastapi import APIRouter, HTTPException, status, UploadFile, File, Depends, Form
    print("   OK")
    
    print("2. Import app.schemas...")
    from app.schemas import UserRegister, UserLogin, TokenResponse, UserOut, StudentProfile
    print("   OK")
    
    print("3. Import app.crud...")
    from app.crud import create_user, find_user_by_email, find_user_by_id, init_text_index
    print("   OK")
    
    print("4. Import app.auth...")
    from app.auth import get_password_hash, verify_password, create_access_token
    print("   OK")
    
    print("5. Import app.utils...")
    from app.utils import get_current_user
    print("   OK")
    
    print("6. Import datetime and os...")
    from datetime import datetime
    import os
    print("   OK")
    
    print("\nAll dependencies imported successfully!")
    print("Now trying direct students.py file execution...")
    
    # Now execute the students file
    with open('app/routes/students.py', 'r') as f:
        code = f.read()
    
    # Create a local namespace to execute in
    namespace = {
        'APIRouter': APIRouter,
        'HTTPException': HTTPException,
        'status': status,
        'UploadFile': UploadFile,
        'File': File,
        'Depends': Depends,
        'Form': Form,
        'UserRegister': UserRegister,
        'UserLogin': UserLogin,
        'TokenResponse': TokenResponse,
        'UserOut': UserOut,
        'StudentProfile': StudentProfile,
        'create_user': create_user,
        'find_user_by_email': find_user_by_email,
        'find_user_by_id': find_user_by_id,
        'init_text_index': init_text_index,
        'get_password_hash': get_password_hash,
        'verify_password': verify_password,
        'create_access_token': create_access_token,
        'get_current_user': get_current_user,
        'datetime': datetime,
        'os': os,
    }
    
    exec(code, namespace)
    
    if 'router' in namespace:
        print(f"SUCCESS: router created = {namespace['router']}")
    else:
        print("ERROR: router not in namespace after exec")
        
except Exception as e:
    print(f"\nEXCEPTION: {e}")
    traceback.print_exc()
