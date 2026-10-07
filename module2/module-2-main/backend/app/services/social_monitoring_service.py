from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models import (
    SocialCandidate,
    SocialDetectionResult,
    SocialDetectionSignal,
    SocialScanJob,
    PlatformEnum,
    SourceTypeEnum,
    ScanStatusEnum,
    ThreatClassificationEnum,
    RiskLevelEnum,
    LookalikePatternEnum,
    OfficialMatchTypeEnum,
    ThreatStatusEnum,
)
from app.schemas import SocialScanRequest, SocialScanJobResponse, SocialCandidateCreate
from app.adapters import get_demo_adapter, DemoSocialAdapter
from app.services.brand_intelligence_client import get_brand_intelligence_client
from app.services.social_detection_service import SocialDetectionService
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class SocialMonitoringService:
    def __init__(self, db: Session):
        self.db = db
        self.detection_service = SocialDetectionService(db)
        self.brand_client = get_brand_intelligence_client()
        self.demo_adapter = get_demo_adapter()

    async def start_scan(self, request: SocialScanRequest) -> SocialScanJobResponse:
        job_id = f"SCAN-{request.brand_id}-{uuid.uuid4().hex[:8].upper()}"
        
        scan_job = SocialScanJob(
            job_id=job_id,
            brand_id=request.brand_id,
            status=ScanStatusEnum.PENDING,
            platforms=[p.value for p in request.platforms] if request.platforms else None,
            total_candidates=0,
            processed_candidates=0,
            threats_found=0,
            official_accounts_found=0,
        )
        self.db.add(scan_job)
        self.db.commit()
        self.db.refresh(scan_job)

        try:
            scan_job.status = ScanStatusEnum.RUNNING
            scan_job.started_at = datetime.utcnow()
            self.db.commit()

            brand_profile = await self.brand_client.get_brand_profile(request.brand_id)
            if not brand_profile:
                raise ValueError(f"Brand profile not found for {request.brand_id}")

            official_accounts = await self.brand_client.get_official_social_accounts(request.brand_id)
            official_usernames = [acc.username for acc in official_accounts]

            if request.use_demo_data or settings.DEMO_MODE:
                adapter = self.demo_adapter
            else:
                adapter = self.demo_adapter

            candidates_data = await adapter.collect_candidates(
                brand_id=request.brand_id,
                brand_name=brand_profile.name,
                official_usernames=official_usernames,
                platforms=request.platforms,
            )

            scan_job.total_candidates = len(candidates_data)
            self.db.commit()

            official_count = 0
            threat_count = 0

            for idx, candidate_data in enumerate(candidates_data):
                scan_job.processed_candidates = idx + 1
                self.db.commit()

                candidate = await self._save_candidate(candidate_data, request.brand_id)
                
                detection_result = await self.detection_service.analyze_candidate(
                    candidate=candidate,
                    brand_profile=brand_profile,
                    official_accounts=official_accounts,
                )

                if detection_result.classification == ThreatClassificationEnum.OFFICIAL:
                    official_count += 1
                else:
                    threat_count += 1

            scan_job.official_accounts_found = official_count
            scan_job.threats_found = threat_count
            scan_job.status = ScanStatusEnum.COMPLETED
            scan_job.completed_at = datetime.utcnow()
            self.db.commit()

        except Exception as e:
            logger.error(f"Scan job {job_id} failed: {e}")
            scan_job.status = ScanStatusEnum.FAILED
            scan_job.error_message = str(e)
            scan_job.completed_at = datetime.utcnow()
            self.db.commit()

        return self._to_job_response(scan_job)

    async def _save_candidate(self, candidate_data, brand_id: str) -> SocialCandidate:
        existing = self.db.query(SocialCandidate).filter(
            SocialCandidate.candidate_id == candidate_data.candidate_id
        ).first()

        if existing:
            for key, value in candidate_data.to_dict().items():
                if hasattr(existing, key) and key not in ["id", "candidate_id", "brand_id"]:
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing

        candidate = SocialCandidate(
            candidate_id=candidate_data.candidate_id,
            brand_id=brand_id,
            platform=candidate_data.platform,
            username=candidate_data.username,
            display_name=candidate_data.display_name,
            profile_url=candidate_data.profile_url,
            bio=candidate_data.bio,
            profile_image_url=candidate_data.profile_image_url,
            logo_image_url=candidate_data.logo_image_url,
            followers_count=candidate_data.followers_count,
            following_count=candidate_data.following_count,
            verification_status=candidate_data.verification_status,
            external_links=candidate_data.external_links,
            contact_information=candidate_data.contact_information,
            collection_source=candidate_data.collection_source,
            collected_at=candidate_data.collected_at or datetime.utcnow(),
        )
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate

    def get_scan_status(self, job_id: str) -> Optional[SocialScanJobResponse]:
        scan_job = self.db.query(SocialScanJob).filter(SocialScanJob.job_id == job_id).first()
        if not scan_job:
            return None
        return self._to_job_response(scan_job)

    def get_scan_history(self, brand_id: str, limit: int = 20) -> List[SocialScanJobResponse]:
        jobs = (
            self.db.query(SocialScanJob)
            .filter(SocialScanJob.brand_id == brand_id)
            .order_by(SocialScanJob.created_at.desc())
            .limit(limit)
            .all()
        )
        return [self._to_job_response(job) for job in jobs]

    def _to_job_response(self, job: SocialScanJob) -> SocialScanJobResponse:
        return SocialScanJobResponse(
            job_id=job.job_id,
            brand_id=job.brand_id,
            status=job.status,
            platforms=[PlatformEnum(p) for p in job.platforms] if job.platforms else None,
            total_candidates=job.total_candidates,
            processed_candidates=job.processed_candidates,
            threats_found=job.threats_found,
            official_accounts_found=job.official_accounts_found,
            error_message=job.error_message,
            started_at=job.started_at,
            completed_at=job.completed_at,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )

    def get_candidates(self, brand_id: str, page: int = 1, page_size: int = 20):
        query = self.db.query(SocialCandidate).filter(SocialCandidate.brand_id == brand_id)
        total = query.count()
        candidates = query.offset((page - 1) * page_size).limit(page_size).all()
        return candidates, total

    def create_candidate(self, candidate_data: SocialCandidateCreate) -> SocialCandidate:
        candidate = SocialCandidate(
            candidate_id=candidate_data.candidate_id,
            brand_id=candidate_data.brand_id,
            platform=candidate_data.platform,
            username=candidate_data.username,
            display_name=candidate_data.display_name,
            profile_url=candidate_data.profile_url,
            bio=candidate_data.bio,
            profile_image_url=candidate_data.profile_image_url,
            logo_image_url=candidate_data.logo_image_url,
            followers_count=candidate_data.followers_count,
            following_count=candidate_data.following_count,
            verification_status=candidate_data.verification_status,
            external_links=candidate_data.external_links,
            contact_information=candidate_data.contact_information,
            collection_source=candidate_data.collection_source,
        )
        self.db.add(candidate)
        self.db.commit()
        self.db.refresh(candidate)
        return candidate