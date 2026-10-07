from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, seed_securebank_demo
from app.routers import brand_registry, social_scan, social_threats, social_candidates
from app.routers import brands as app_monitoring_brands, apps as app_routers, scans, detection


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_securebank_demo()
    yield


app = FastAPI(
    title="AI-Powered Digital Risk Protection Platform",
    description="Unified API for brand intelligence, social monitoring, and app store monitoring.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "digital-risk-protection-platform",
        "brand_registry": "healthy",
        "social_monitoring": "healthy",
        "app_monitoring": "healthy",
    }


@app.get("/")
async def root():
    return {
        "service": "AI-Powered Digital Risk Protection Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


app.include_router(brand_registry.router, prefix="/api", tags=["Brand Registry"])
app.include_router(social_scan.router, prefix="/api", tags=["Social Scan"])
app.include_router(social_threats.router, prefix="/api", tags=["Social Threats"])
app.include_router(social_candidates.router, prefix="/api", tags=["Social Candidates"])
app.include_router(app_monitoring_brands.router, prefix="/api/app-monitoring", tags=["App Monitoring Brands"])
app.include_router(app_routers.router, prefix="/api/apps", tags=["Apps"])
app.include_router(scans.router, prefix="/api/scans", tags=["Scans"])
app.include_router(detection.router, prefix="/api/detection", tags=["Detection"])
