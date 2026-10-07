from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SocialScanRequest, SocialScanJobResponse, PlatformEnum
from app.services.social_monitoring_service import SocialMonitoringService
from app.models import ScanStatusEnum
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_monitoring_service(db: Session = Depends(get_db)) -> SocialMonitoringService:
    return SocialMonitoringService(db)


@router.post("/scan", response_model=SocialScanJobResponse, tags=["Social Scan"])
async def run_scan(
    request: SocialScanRequest,
    service: SocialMonitoringService = Depends(get_monitoring_service),
):
    try:
        job = await service.start_scan(request)
        return job
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scan/{job_id}", response_model=SocialScanJobResponse, tags=["Social Scan"])
async def get_scan_status(
    job_id: str,
    service: SocialMonitoringService = Depends(get_monitoring_service),
):
    job = service.get_scan_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Scan job not found")
    return job


@router.get("/scan/history/{brand_id}", response_model=list[SocialScanJobResponse], tags=["Social Scan"])
async def get_scan_history(
    brand_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    service: SocialMonitoringService = Depends(get_monitoring_service),
):
    return service.get_scan_history(brand_id, limit=limit)
