from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from app.data import get_brand, list_brands, BRAND_ID

app = FastAPI(
    title="Module 1: Brand Intelligence & Official Brand Assets",
    description="Digital Risk Protection Platform - Module 1 Brand Registry API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "Brand Intelligence & Official Brand Assets",
        "module": 1,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "brand-intelligence", "module": 1}


@app.get("/api/brands", response_model=List[Dict[str, Any]])
async def get_brands():
    return list_brands()


@app.get("/api/brands/{brand_id}", response_model=Dict[str, Any])
async def get_brand_profile(brand_id: str):
    profile = get_brand(brand_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Brand '{brand_id}' not found")
    return profile


@app.get("/api/brands/{brand_id}/fingerprint", response_model=Dict[str, Any])
async def get_brand_fingerprint(brand_id: str):
    profile = get_brand(brand_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Brand '{brand_id}' not found")
    return profile.get("brand_fingerprint", {})
