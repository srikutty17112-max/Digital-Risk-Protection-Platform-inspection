from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from enum import Enum


class PlatformEnum(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    X_TWITTER = "x_twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    OTHER = "other"


class SourceTypeEnum(str, Enum):
    LIVE = "LIVE"
    DEMO = "DEMO"
    IMPORTED = "IMPORTED"
    API = "API"
    MOCK = "MOCK"


class ScanStatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class ThreatClassificationEnum(str, Enum):
    OFFICIAL = "OFFICIAL"
    LIKELY_LEGITIMATE = "LIKELY_LEGITIMATE"
    SUSPICIOUS = "SUSPICIOUS"
    LIKELY_IMPERSONATION = "LIKELY_IMPERSONATION"
    HIGH_RISK_IMPERSONATION = "HIGH_RISK_IMPERSONATION"


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LookalikePatternEnum(str, Enum):
    CHARACTER_SWAP = "CHARACTER_SWAP"
    ADDED_WORD = "ADDED_WORD"
    REMOVED_CHARACTER = "REMOVED_CHARACTER"
    EXTRA_CHARACTER = "EXTRA_CHARACTER"
    SPACING_CHANGE = "SPACING_CHANGE"
    PUNCTUATION_CHANGE = "PUNCTUATION_CHANGE"
    CHARACTER_SUBSTITUTION = "CHARACTER_SUBSTITUTION"
    CASE_VARIATION = "CASE_VARIATION"


class OfficialMatchTypeEnum(str, Enum):
    EXACT = "EXACT"
    PARTIAL = "PARTIAL"
    NONE = "NONE"


class ThreatStatusEnum(str, Enum):
    NEW = "NEW"
    REVIEWED = "REVIEWED"
    DISMISSED = "DISMISSED"
    CONFIRMED = "CONFIRMED"
    ESCALATED = "ESCALATED"


class SocialCandidateBase(BaseModel):
    brand_id: str = Field(..., description="Brand identifier")
    platform: PlatformEnum
    username: Optional[str] = None
    display_name: Optional[str] = None
    profile_url: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    logo_image_url: Optional[str] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    verification_status: Optional[str] = None
    external_links: Optional[List[str]] = None
    contact_information: Optional[Dict[str, Any]] = None
    collection_source: SourceTypeEnum


class SocialCandidateCreate(SocialCandidateBase):
    candidate_id: str = Field(..., description="Unique candidate identifier")


class SocialCandidateResponse(SocialCandidateBase):
    candidate_id: str
    collected_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SocialCandidateListResponse(BaseModel):
    candidates: List[SocialCandidateResponse]
    total: int
    page: int
    page_size: int


class SocialScanRequest(BaseModel):
    brand_id: str
    platforms: Optional[List[PlatformEnum]] = None
    use_demo_data: bool = True


class SocialScanJobResponse(BaseModel):
    job_id: str
    brand_id: str
    status: ScanStatusEnum
    platforms: Optional[List[PlatformEnum]] = None
    total_candidates: int
    processed_candidates: int
    threats_found: int
    official_accounts_found: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfficialMatchResponse(BaseModel):
    is_official: bool
    matched_asset_id: Optional[str] = None
    match_type: OfficialMatchTypeEnum
    confidence: float


class LookalikeResponse(BaseModel):
    detected: bool
    pattern: Optional[LookalikePatternEnum] = None
    similarity: Optional[float] = None
    explanation: Optional[str] = None


class SignalsResponse(BaseModel):
    name_similarity: Optional[float] = None
    logo_similarity: Optional[float] = None
    branding_similarity: Optional[float] = None
    external_domain_similarity: Optional[float] = None


class CandidateSummaryResponse(BaseModel):
    username: Optional[str] = None
    display_name: Optional[str] = None
    profile_url: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None


class SocialThreatResponse(BaseModel):
    id: str
    brand_id: str
    source_type: str
    platform: PlatformEnum

    candidate: CandidateSummaryResponse

    signals: SignalsResponse

    lookalike: LookalikeResponse

    official_match: OfficialMatchResponse

    risk_score: float
    risk_level: RiskLevelEnum
    confidence: float

    classification: ThreatClassificationEnum

    reasons: List[str]

    source: Dict[str, Any]

    status: ThreatStatusEnum

    model_config = ConfigDict(from_attributes=True)


class SocialThreatListResponse(BaseModel):
    threats: List[SocialThreatResponse]
    total: int
    page: int
    page_size: int


class SocialThreatDetailResponse(SocialThreatResponse):
    collected_at: datetime


class ScanProgressResponse(BaseModel):
    stage: str
    progress: int
    message: str