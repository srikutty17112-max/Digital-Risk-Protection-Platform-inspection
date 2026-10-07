from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, engine
from app.models import Base
from app.routes import social_scan, social_threats, social_candidates


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(social_scan.router, prefix="/api", tags=["Social Scan"])
app.include_router(social_threats.router, prefix="/api", tags=["Social Threats"])
app.include_router(social_candidates.router, prefix="/api", tags=["Social Candidates"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "social-media-monitoring",
        "version": settings.PROJECT_VERSION,
        "demo_mode": settings.DEMO_MODE,
    }


@app.get("/")
async def root():
    return {
        "service": "BrandShield Social Media Monitoring & Impersonation Detection",
        "module": 2,
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "health": "/health",
    }