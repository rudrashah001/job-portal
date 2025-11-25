import sys
import traceback

print("Executing main.py step by step...\n")

try:
    print("1. Import FastAPI...")
    from fastapi import FastAPI
    print("   OK")
    
    print("2. Import CORS middleware...")
    from fastapi.middleware.cors import CORSMiddleware
    print("   OK")
    
    print("3. Import uvicorn...")
    import uvicorn
    print("   OK")
    
    print("4. Import app.routes...")
    from app.routes import students, recruiters, jobs, admin
    print(f"   OK - students: {hasattr(students, 'router')}, recruiters: {hasattr(recruiters, 'router')}, jobs: {hasattr(jobs, 'router')}, admin: {hasattr(admin, 'router')}")
    
    print("5. Create FastAPI app...")
    app = FastAPI(title="Campus Job Portal - Backend")
    print(f"   OK, app = {app}")
    
    print("6. Add CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("   OK")
    
    print("7. Include routers...")
    app.include_router(students.router, prefix="/api/students", tags=["students"])
    app.include_router(recruiters.router, prefix="/api/recruiters", tags=["recruiters"])
    app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    print("   OK")
    
    print("\nSUCCESS: All steps completed!")
    print(f"app = {app}")
    print(f"app.routes = {len(app.routes)}")
    
except Exception as e:
    print(f"\nERROR at some step: {e}")
    traceback.print_exc()
