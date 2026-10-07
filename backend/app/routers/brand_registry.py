from fastapi import APIRouter
from typing import List, Dict, Any
from app.services.brand.registry import brand_registry

router = APIRouter()


@router.get("/brands", response_model=List[Dict[str, Any]])
async def get_brands():
    return brand_registry.list_brands()


@router.get("/brands/{brand_id}", response_model=Dict[str, Any])
async def get_brand_profile(brand_id: str):
    profile = brand_registry.get_brand(brand_id)
    if not profile:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Brand '{brand_id}' not found")
    return profile


@router.get("/brands/{brand_id}/fingerprint", response_model=Dict[str, Any])
async def get_brand_fingerprint(brand_id: str):
    profile = brand_registry.get_brand(brand_id)
    if not profile:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Brand '{brand_id}' not found")
    return profile.get("brand_fingerprint", {})
