import sys
import traceback

# Add debug
try:
    print("Step 1: Import FastAPI")
    from fastapi import FastAPI
    print("  OK")
    
    print("Step 2: Import CORS middleware")
    from fastapi.middleware.cors import CORSMiddleware
    print("  OK")
    
    print("Step 3: Import uvicorn")
    import uvicorn
    print("  OK")
    
    print("Step 4: Import routers")
    from app.routes import students, recruiters, jobs, admin
    print("  OK")
    
    print("Step 5: Create FastAPI app")
    app = FastAPI(title="Campus Job Portal - Backend")
    print(f"  OK, app = {app}")
    
    print("Step 6: Add CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("  OK")
    
    print("Step 7: Include routers")
    app.include_router(students.router, prefix="/api/students", tags=["students"])
    app.include_router(recruiters.router, prefix="/api/recruiters", tags=["recruiters"])
    app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
    print("  OK")
    
    print("SUCCESS: All steps completed. app is ready.")
    print(f"app = {app}")
    
except Exception as e:
    print(f"ERROR at some step: {e}")
    traceback.print_exc()
