from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routes import auth, health

from .routes import auth, health, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RoadPulse API",
    description="AI-powered pothole reporting and road safety platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.include_router(
    health.router,
    prefix="/api",
)

app.include_router(
    auth.router,
    prefix="/api",
)

app.include_router(
    reports.router,
    prefix="/api",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to RoadPulse",
        "status": "running",
    }