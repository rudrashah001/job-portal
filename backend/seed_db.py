import asyncio
import os
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def seed_database():
    """Seed the database with sample jobs."""
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["AuthDB"]
    jobs_col = db["jobs"]
    
    # Sample jobs
    sample_jobs = [
        {
            "title": "Senior Python Developer",
            "description": "We are looking for an experienced Python developer to join our backend team.",
            "company_name": "Tech Innovations Inc",
            "location": "San Francisco, CA",
            "employment_type": "Full-time",
            "skills_required": ["Python", "FastAPI", "MongoDB", "Docker"],
            "application_deadline": datetime.utcnow() + timedelta(days=30),
            "posted_by": "recruiter1",
            "posted_at": datetime.utcnow(),
            "applicants": []
        },
        {
            "title": "React Frontend Engineer",
            "description": "Join our frontend team to build beautiful, responsive web applications.",
            "company_name": "Digital Solutions Ltd",
            "location": "New York, NY",
            "employment_type": "Full-time",
            "skills_required": ["React", "JavaScript", "CSS", "REST APIs"],
            "application_deadline": datetime.utcnow() + timedelta(days=25),
            "posted_by": "recruiter2",
            "posted_at": datetime.utcnow(),
            "applicants": []
        },
        {
            "title": "Full Stack Developer",
            "description": "Develop and maintain full stack applications using modern tech stack.",
            "company_name": "StartupXYZ",
            "location": "Remote",
            "employment_type": "Full-time",
            "skills_required": ["Python", "React", "PostgreSQL", "Git"],
            "application_deadline": datetime.utcnow() + timedelta(days=20),
            "posted_by": "recruiter1",
            "posted_at": datetime.utcnow(),
            "applicants": []
        },
        {
            "title": "Data Scientist",
            "description": "Analyze large datasets and build machine learning models.",
            "company_name": "Data Analytics Co",
            "location": "Boston, MA",
            "employment_type": "Full-time",
            "skills_required": ["Python", "Machine Learning", "SQL", "Statistics"],
            "application_deadline": datetime.utcnow() + timedelta(days=35),
            "posted_by": "recruiter3",
            "posted_at": datetime.utcnow(),
            "applicants": []
        },
        {
            "title": "DevOps Engineer",
            "description": "Manage cloud infrastructure and CI/CD pipelines.",
            "company_name": "Cloud Services Pro",
            "location": "Seattle, WA",
            "employment_type": "Full-time",
            "skills_required": ["AWS", "Docker", "Kubernetes", "Terraform"],
            "application_deadline": datetime.utcnow() + timedelta(days=28),
            "posted_by": "recruiter2",
            "posted_at": datetime.utcnow(),
            "applicants": []
        }
    ]
    
    try:
        result = await jobs_col.insert_many(sample_jobs)
        print(f"Success! Inserted {len(result.inserted_ids)} sample jobs into MongoDB")
        print(f"Job IDs: {[str(id) for id in result.inserted_ids]}")
        
        # Create text index for search
        await jobs_col.create_index([("title", "text"), ("description", "text")])
        print("Created text index for full-text search")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
