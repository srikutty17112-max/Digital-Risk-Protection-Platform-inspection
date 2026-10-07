from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    SocialThreatResponse,
    SocialThreatListResponse,
    SocialThreatDetailResponse,
    ThreatStatusEnum,
)
from app.services.social_detection_service import SocialDetectionService
from app.services.brand_intelligence_client import get_brand_intelligence_client
from app.models import SocialDetectionResult, SocialCandidate, ThreatStatusEnum as ModelThreatStatusEnum
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/threats", response_model=SocialThreatListResponse, tags=["Social Threats"])
async def list_threats(
    brand_id: str = Query(...),
    classification: Optional[str] = Query(default=None),
    risk_level: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    include_official: bool = Query(default=False),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(SocialDetectionResult).filter(SocialDetectionResult.brand_id == brand_id)

    if classification:
        query = query.filter(SocialDetectionResult.classification == classification)
    if risk_level:
        query = query.filter(SocialDetectionResult.risk_level == risk_level)
    if status:
        query = query.filter(SocialDetectionResult.status == status)

    if not include_official:
        query = query.filter(SocialDetectionResult.classification != "OFFICIAL")

    total = query.count()
    offset = (page - 1) * page_size
    results = query.order_by(SocialDetectionResult.created_at.desc()).offset(offset).limit(page_size).all()

    threats = []
    for result in results:
        candidate = db.query(SocialCandidate).filter(SocialCandidate.id == result.candidate_id).first()
        if not candidate:
            continue

        threats.append(SocialThreatResponse(
            id=result.threat_id,
            brand_id=result.brand_id,
            source_type=result.source_type.value,
            platform=candidate.platform,
            candidate={
                "username": candidate.username,
                "display_name": candidate.display_name,
                "profile_url": candidate.profile_url,
                "bio": candidate.bio,
                "profile_image_url": candidate.profile_image_url,
            },
            signals={
                "name_similarity": result.name_similarity,
                "logo_similarity": result.logo_similarity,
                "branding_similarity": result.branding_similarity,
                "external_domain_similarity": result.external_domain_similarity,
            },
            lookalike={
                "detected": result.lookalike_detected,
                "pattern": result.lookalike_pattern.value if result.lookalike_pattern else None,
                "similarity": result.lookalike_similarity,
                "explanation": result.lookalike_explanation,
            },
            official_match={
                "is_official": result.official_match_is_official,
                "matched_asset_id": result.official_match_asset_id,
                "match_type": result.official_match_type.value,
                "confidence": result.official_match_confidence,
            },
            risk_score=result.risk_score,
            risk_level=result.risk_level.value,
            confidence=result.confidence,
            classification=result.classification.value,
            reasons=result.reasons or [],
            source={},
            status=result.status.value,
        ))

    return SocialThreatListResponse(threats=threats, total=total, page=page, page_size=page_size)


@router.get("/threats/{threat_id}", response_model=SocialThreatDetailResponse, tags=["Social Threats"])
async def get_threat_detail(
    threat_id: str,
    db: Session = Depends(get_db),
):
    result = db.query(SocialDetectionResult).filter(SocialDetectionResult.threat_id == threat_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Threat not found")

    candidate = db.query(SocialCandidate).filter(SocialCandidate.id == result.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return SocialThreatDetailResponse(
        id=result.threat_id,
        brand_id=result.brand_id,
        source_type=result.source_type.value,
        platform=candidate.platform,
        candidate={
            "username": candidate.username,
            "display_name": candidate.display_name,
            "profile_url": candidate.profile_url,
            "bio": candidate.bio,
            "profile_image_url": candidate.profile_image_url,
        },
        signals={
            "name_similarity": result.name_similarity,
            "logo_similarity": result.logo_similarity,
            "branding_similarity": result.branding_similarity,
            "external_domain_similarity": result.external_domain_similarity,
        },
        lookalike={
            "detected": result.lookalike_detected,
            "pattern": result.lookalike_pattern.value if result.lookalike_pattern else None,
            "similarity": result.lookalike_similarity,
            "explanation": result.lookalike_explanation,
        },
        official_match={
            "is_official": result.official_match_is_official,
            "matched_asset_id": result.official_match_asset_id,
            "match_type": result.official_match_type.value,
            "confidence": result.official_match_confidence,
        },
        risk_score=result.risk_score,
        risk_level=result.risk_level.value,
        confidence=result.confidence,
        classification=result.classification.value,
        reasons=result.reasons or [],
        source={},
        status=result.status.value,
        collected_at=result.collected_at,
    )


@router.patch("/threats/{threat_id}/status", response_model=SocialThreatDetailResponse, tags=["Social Threats"])
async def update_threat_status(
    threat_id: str,
    new_status: ThreatStatusEnum = Query(...),
    db: Session = Depends(get_db),
):
    result = db.query(SocialDetectionResult).filter(SocialDetectionResult.threat_id == threat_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Threat not found")

    result.status = ModelThreatStatusEnum[new_status.value]
    db.commit()
    db.refresh(result)

    candidate = db.query(SocialCandidate).filter(SocialCandidate.id == result.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return SocialThreatDetailResponse(
        id=result.threat_id,
        brand_id=result.brand_id,
        source_type=result.source_type.value,
        platform=candidate.platform,
        candidate={
            "username": candidate.username,
            "display_name": candidate.display_name,
            "profile_url": candidate.profile_url,
            "bio": candidate.bio,
            "profile_image_url": candidate.profile_image_url,
        },
        signals={
            "name_similarity": result.name_similarity,
            "logo_similarity": result.logo_similarity,
            "branding_similarity": result.branding_similarity,
            "external_domain_similarity": result.external_domain_similarity,
        },
        lookalike={
            "detected": result.lookalike_detected,
            "pattern": result.lookalike_pattern.value if result.lookalike_pattern else None,
            "similarity": result.lookalike_similarity,
            "explanation": result.lookalike_explanation,
        },
        official_match={
            "is_official": result.official_match_is_official,
            "matched_asset_id": result.official_match_asset_id,
            "match_type": result.official_match_type.value,
            "confidence": result.official_match_confidence,
        },
        risk_score=result.risk_score,
        risk_level=result.risk_level.value,
        confidence=result.confidence,
        classification=result.classification.value,
        reasons=result.reasons or [],
        source={},
        status=result.status.value,
        collected_at=result.collected_at,
    )
