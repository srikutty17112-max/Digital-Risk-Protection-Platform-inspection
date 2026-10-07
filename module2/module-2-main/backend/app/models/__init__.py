import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Index,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.orm import relationship, declarative_base
from app.database import Base


class PlatformEnum(str, enum.Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    X_TWITTER = "x_twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    OTHER = "other"


class SourceTypeEnum(str, enum.Enum):
    LIVE = "LIVE"
    DEMO = "DEMO"
    IMPORTED = "IMPORTED"
    API = "API"
    MOCK = "MOCK"


class ScanStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class ThreatClassificationEnum(str, enum.Enum):
    OFFICIAL = "OFFICIAL"
    LIKELY_LEGITIMATE = "LIKELY_LEGITIMATE"
    SUSPICIOUS = "SUSPICIOUS"
    LIKELY_IMPERSONATION = "LIKELY_IMPERSONATION"
    HIGH_RISK_IMPERSONATION = "HIGH_RISK_IMPERSONATION"


class RiskLevelEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LookalikePatternEnum(str, enum.Enum):
    CHARACTER_SWAP = "CHARACTER_SWAP"
    ADDED_WORD = "ADDED_WORD"
    REMOVED_CHARACTER = "REMOVED_CHARACTER"
    EXTRA_CHARACTER = "EXTRA_CHARACTER"
    SPACING_CHANGE = "SPACING_CHANGE"
    PUNCTUATION_CHANGE = "PUNCTUATION_CHANGE"
    CHARACTER_SUBSTITUTION = "CHARACTER_SUBSTITUTION"
    CASE_VARIATION = "CASE_VARIATION"


class OfficialMatchTypeEnum(str, enum.Enum):
    EXACT = "EXACT"
    PARTIAL = "PARTIAL"
    NONE = "NONE"


class ThreatStatusEnum(str, enum.Enum):
    NEW = "NEW"
    REVIEWED = "REVIEWED"
    DISMISSED = "DISMISSED"
    CONFIRMED = "CONFIRMED"
    ESCALATED = "ESCALATED"


class SocialCandidate(Base):
    __tablename__ = "social_candidates"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String(100), unique=True, index=True, nullable=False)
    brand_id = Column(String(100), index=True, nullable=False)
    platform = Column(SQLEnum(PlatformEnum), index=True, nullable=False)
    username = Column(String(255), nullable=True)
    display_name = Column(String(255), nullable=True)
    profile_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    logo_image_url = Column(String(500), nullable=True)
    followers_count = Column(Integer, nullable=True)
    following_count = Column(Integer, nullable=True)
    verification_status = Column(String(50), nullable=True)
    external_links = Column(JSON, nullable=True)
    contact_information = Column(JSON, nullable=True)
    collection_source = Column(SQLEnum(SourceTypeEnum), nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    detection_results = relationship("SocialDetectionResult", back_populates="candidate", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_social_candidates_brand_platform", "brand_id", "platform"),
        Index("ix_social_candidates_collected_at", "collected_at"),
    )


class SocialDetectionSignal(Base):
    __tablename__ = "social_detection_signals"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("social_detection_results.id"), nullable=False, index=True)
    name_similarity = Column(Float, nullable=True)
    logo_similarity = Column(Float, nullable=True)
    branding_similarity = Column(Float, nullable=True)
    external_domain_similarity = Column(Float, nullable=True)
    identifier_mismatch_score = Column(Float, nullable=True)
    official_mismatch = Column(Boolean, default=True, nullable=False)
    raw_signals = Column(JSON, nullable=True)

    result = relationship("SocialDetectionResult", back_populates="signals")


class SocialDetectionResult(Base):
    __tablename__ = "social_detection_results"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(String(100), unique=True, index=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("social_candidates.id"), nullable=False, index=True)
    brand_id = Column(String(100), index=True, nullable=False)

    name_similarity = Column(Float, nullable=True)
    logo_similarity = Column(Float, nullable=True)
    branding_similarity = Column(Float, nullable=True)
    external_domain_similarity = Column(Float, nullable=True)

    lookalike_detected = Column(Boolean, default=False, nullable=False)
    lookalike_pattern = Column(SQLEnum(LookalikePatternEnum), nullable=True)
    lookalike_similarity = Column(Float, nullable=True)
    lookalike_explanation = Column(Text, nullable=True)

    official_match_is_official = Column(Boolean, default=False, nullable=False)
    official_match_asset_id = Column(String(100), nullable=True)
    official_match_type = Column(SQLEnum(OfficialMatchTypeEnum), default=OfficialMatchTypeEnum.NONE, nullable=False)
    official_match_confidence = Column(Float, default=0.0, nullable=False)

    risk_score = Column(Float, default=0.0, nullable=False)
    risk_level = Column(SQLEnum(RiskLevelEnum), default=RiskLevelEnum.LOW, nullable=False)
    confidence = Column(Float, default=0.0, nullable=False)
    classification = Column(SQLEnum(ThreatClassificationEnum), default=ThreatClassificationEnum.LIKELY_LEGITIMATE, nullable=False)
    reasons = Column(JSON, nullable=True)

    source_type = Column(SQLEnum(SourceTypeEnum), nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    status = Column(SQLEnum(ThreatStatusEnum), default=ThreatStatusEnum.NEW, nullable=False)

    candidate = relationship("SocialCandidate", back_populates="detection_results")
    signals = relationship("SocialDetectionSignal", back_populates="result", cascade="all, delete-orphan", uselist=False)

    __table_args__ = (
        Index("ix_social_detection_results_brand_classification", "brand_id", "classification"),
        Index("ix_social_detection_results_risk_level", "risk_level"),
        Index("ix_social_detection_results_created_at", "created_at"),
    )


class SocialScanJob(Base):
    __tablename__ = "social_scan_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(100), unique=True, index=True, nullable=False)
    brand_id = Column(String(100), index=True, nullable=False)
    status = Column(SQLEnum(ScanStatusEnum), default=ScanStatusEnum.PENDING, nullable=False)
    platforms = Column(JSON, nullable=True)
    total_candidates = Column(Integer, default=0, nullable=False)
    processed_candidates = Column(Integer, default=0, nullable=False)
    threats_found = Column(Integer, default=0, nullable=False)
    official_accounts_found = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_social_scan_jobs_brand_status", "brand_id", "status"),
        Index("ix_social_scan_jobs_created_at", "created_at"),
    )