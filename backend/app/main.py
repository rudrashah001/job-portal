from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routes import students, recruiters, jobs, admin

app = FastAPI(title="Campus Job Portal - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(recruiters.router, prefix="/api/recruiters", tags=["recruiters"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/")
async def root():
    return {"status": "ok", "app": "Campus Job Portal Backend"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


