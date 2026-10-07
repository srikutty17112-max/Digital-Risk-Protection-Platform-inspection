from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SocialCandidateCreate, SocialCandidateResponse, SocialCandidateListResponse
from app.services.social_monitoring_service import SocialMonitoringService
from app.models import SocialCandidate
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/candidates", response_model=SocialCandidateListResponse, tags=["Social Candidates"])
async def list_candidates(
    brand_id: str = Query(...),
    platform: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(SocialCandidate).filter(SocialCandidate.brand_id == brand_id)
    if platform:
        query = query.filter(SocialCandidate.platform == platform)

    total = query.count()
    offset = (page - 1) * page_size
    candidates = query.order_by(SocialCandidate.collected_at.desc()).offset(offset).limit(page_size).all()

    items = []
    for c in candidates:
        items.append(SocialCandidateResponse(
            candidate_id=c.candidate_id,
            brand_id=c.brand_id,
            platform=c.platform,
            username=c.username,
            display_name=c.display_name,
            profile_url=c.profile_url,
            bio=c.bio,
            profile_image_url=c.profile_image_url,
            logo_image_url=c.logo_image_url,
            followers_count=c.followers_count,
            following_count=c.following_count,
            verification_status=c.verification_status,
            external_links=c.external_links,
            contact_information=c.contact_information,
            collection_source=c.collection_source,
            collected_at=c.collected_at,
            updated_at=c.updated_at,
        ))

    return SocialCandidateListResponse(candidates=items, total=total, page=page, page_size=page_size)


@router.post("/candidates", response_model=SocialCandidateResponse, tags=["Social Candidates"])
async def add_candidate(
    data: SocialCandidateCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(SocialCandidate).filter(SocialCandidate.candidate_id == data.candidate_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Candidate already exists")

    candidate = SocialCandidate(
        candidate_id=data.candidate_id,
        brand_id=data.brand_id,
        platform=data.platform,
        username=data.username,
        display_name=data.display_name,
        profile_url=data.profile_url,
        bio=data.bio,
        profile_image_url=data.profile_image_url,
        logo_image_url=data.logo_image_url,
        followers_count=data.followers_count,
        following_count=data.following_count,
        verification_status=data.verification_status,
        external_links=data.external_links,
        contact_information=data.contact_information,
        collection_source=data.collection_source,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return SocialCandidateResponse(
        candidate_id=candidate.candidate_id,
        brand_id=candidate.brand_id,
        platform=candidate.platform,
        username=candidate.username,
        display_name=candidate.display_name,
        profile_url=candidate.profile_url,
        bio=candidate.bio,
        profile_image_url=candidate.profile_image_url,
        logo_image_url=candidate.logo_image_url,
        followers_count=candidate.followers_count,
        following_count=candidate.following_count,
            verification_status=candidate.verification_status,
            external_links=candidate.external_links,
            contact_information=candidate.contact_information,
            collection_source=candidate.collection_source,
            collected_at=candidate.collected_at,
            updated_at=candidate.updated_at,
        )


@router.get("/candidates/{candidate_id}", response_model=SocialCandidateResponse, tags=["Social Candidates"])
async def get_candidate(
    candidate_id: str,
    db: Session = Depends(get_db),
):
    candidate = db.query(SocialCandidate).filter(SocialCandidate.candidate_id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return SocialCandidateResponse(
        candidate_id=candidate.candidate_id,
        brand_id=candidate.brand_id,
        platform=candidate.platform,
        username=candidate.username,
        display_name=candidate.display_name,
        profile_url=candidate.profile_url,
        bio=candidate.bio,
        profile_image_url=candidate.profile_image_url,
        logo_image_url=candidate.logo_image_url,
        followers_count=candidate.followers_count,
        following_count=candidate.following_count,
        verification_status=candidate.verification_status,
        external_links=candidate.external_links,
        contact_information=candidate.contact_information,
        collection_source=candidate.collection_source,
        collected_at=candidate.collected_at,
        updated_at=candidate.updated_at,
    )
