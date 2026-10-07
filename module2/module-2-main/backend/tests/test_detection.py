import pytest
import asyncio
from app.services.social_detection_service import SocialDetectionService
from app.models import (
    SocialCandidate,
    PlatformEnum,
    SourceTypeEnum,
)
from app.services.brand_intelligence_client import BrandProfile, OfficialSocialAccount
from sqlalchemy.orm import Session


class TestOfficialAccountExclusion:
    @pytest.fixture
    def db_session(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.database import Base

        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

    @pytest.mark.asyncio
    async def test_official_account_not_flagged(self, db_session: Session):
        brand_profile = BrandProfile(
            brand_id="KAMPUSVC",
            name="KampusVC",
            official_domain="kampus.vc",
            logo_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            brand_keywords=["venture capital", "student startups", "funding", "founders", "university"],
            aliases=["Kampus VC", "Kampus.VC", "KV"],
            registered_names=["KampusVC Inc.", "Kampus Venture Capital"],
            contact_email="hello@kampus.vc",
            contact_phone="+1-555-0100",
            description="Venture capital fund investing in student-founded startups",
        )
        official_accounts = [
            OfficialSocialAccount(
                platform="instagram",
                username="kampusvc",
                display_name="KampusVC",
                profile_url="https://instagram.com/kampusvc",
                verified=True,
                asset_id="ASSET-KAMPUSVC-INSTA-001",
            )
        ]
        candidate = SocialCandidate(
            candidate_id="DEMO-KAMPUSVC-INSTA-001",
            brand_id="KAMPUSVC",
            platform=PlatformEnum.INSTAGRAM,
            username="kampusvc",
            display_name="KampusVC",
            profile_url="https://instagram.com/kampusvc",
            bio="Official KampusVC - Venture capital for student startups.",
            profile_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            logo_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            followers_count=12500,
            following_count=342,
            verification_status="verified",
            external_links=["https://kampus.vc", "https://linkedin.com/company/kampusvc"],
            contact_information={"email": "hello@kampus.vc", "website": "https://kampus.vc"},
            collection_source=SourceTypeEnum.DEMO,
        )
        db_session.add(candidate)
        db_session.commit()
        db_session.refresh(candidate)

        service = SocialDetectionService(db_session)
        result = await service.analyze_candidate(candidate, brand_profile, official_accounts)

        assert result.classification.value == "OFFICIAL"
        assert result.risk_score == 0.0
        assert result.confidence == 1.0
        assert result.official_match_is_official is True

    @pytest.mark.asyncio
    async def test_impersonation_not_official(self, db_session: Session):
        brand_profile = BrandProfile(
            brand_id="KAMPUSVC",
            name="KampusVC",
            official_domain="kampus.vc",
            logo_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            brand_keywords=["venture capital", "student startups", "funding", "founders", "university"],
            aliases=["Kampus VC", "Kampus.VC", "KV"],
            registered_names=["KampusVC Inc.", "Kampus Venture Capital"],
            contact_email="hello@kampus.vc",
            contact_phone="+1-555-0100",
        )
        official_accounts = [
            OfficialSocialAccount(
                platform="instagram",
                username="kampusvc",
                display_name="KampusVC",
                profile_url="https://instagram.com/kampusvc",
                verified=True,
                asset_id="ASSET-KAMPUSVC-INSTA-001",
            )
        ]
        candidate = SocialCandidate(
            candidate_id="DEMO-KAMPUSVC-INSTA-002",
            brand_id="KAMPUSVC",
            platform=PlatformEnum.INSTAGRAM,
            username="kampussvc",
            display_name="KampussVC",
            profile_url="https://instagram.com/kampussvc",
            bio="KampussVC - Student venture capital and startup funding.",
            profile_image_url="https://demo-assets.brandshield.io/kampusvc/logo_similar_1.png",
            logo_image_url="https://demo-assets.brandshield.io/kampusvc/logo_similar_1.png",
            followers_count=3420,
            following_count=1200,
            verification_status="none",
            external_links=["https://kampussvc.com", "https://kampus-vc-login.com"],
            contact_information={"email": "support@kampussvc.com", "phone": "+1-555-0199"},
            collection_source=SourceTypeEnum.DEMO,
        )
        db_session.add(candidate)
        db_session.commit()
        db_session.refresh(candidate)

        service = SocialDetectionService(db_session)
        result = await service.analyze_candidate(candidate, brand_profile, official_accounts)

        assert result.classification.value != "OFFICIAL"
        assert result.official_match_is_official is False
        assert result.risk_score > 0


class TestContactMismatch:
    def test_email_domain_mismatch(self):
        from app.services.social_detection_service import SocialDetectionService
        from app.models import SocialCandidate, PlatformEnum, SourceTypeEnum
        from app.services.brand_intelligence_client import BrandProfile, OfficialSocialAccount
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.database import Base

        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        brand_profile = BrandProfile(
            brand_id="KAMPUSVC",
            name="KampusVC",
            official_domain="kampus.vc",
            contact_phone="+1-555-0100",
        )
        official_accounts = []
        candidate = SocialCandidate(
            candidate_id="DEMO-MISMATCH-001",
            brand_id="KAMPUSVC",
            platform=PlatformEnum.INSTAGRAM,
            username="kampusvc_suspicious",
            display_name="KampusVC Suspicious",
            profile_url="https://instagram.com/kampusvc_suspicious",
            bio="Suspicious account",
            profile_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            logo_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            followers_count=100,
            following_count=50,
            verification_status="none",
            external_links=["https://suspicious-domain.com"],
            contact_information={"email": "contact@wrong-domain.com", "phone": "+1-555-9999"},
            collection_source=SourceTypeEnum.DEMO,
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        service = SocialDetectionService(db)
        mismatch = service._check_identifier_mismatch(candidate, brand_profile)
        assert mismatch is True

        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

    def test_phone_mismatch(self):
        from app.services.social_detection_service import SocialDetectionService
        from app.models import SocialCandidate, PlatformEnum, SourceTypeEnum
        from app.services.brand_intelligence_client import BrandProfile
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.database import Base

        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        brand_profile = BrandProfile(
            brand_id="KAMPUSVC",
            name="KampusVC",
            official_domain="kampus.vc",
            contact_phone="+1-555-0100",
        )
        candidate = SocialCandidate(
            candidate_id="DEMO-MISMATCH-002",
            brand_id="KAMPUSVC",
            platform=PlatformEnum.INSTAGRAM,
            username="kampusvc_suspicious",
            display_name="KampusVC Suspicious",
            profile_url="https://instagram.com/kampusvc_suspicious",
            bio="Suspicious account",
            profile_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            logo_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            followers_count=100,
            following_count=50,
            verification_status="none",
            external_links=[],
            contact_information={"email": "hello@kampus.vc", "phone": "+1-555-9999"},
            collection_source=SourceTypeEnum.DEMO,
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        service = SocialDetectionService(db)
        mismatch = service._check_identifier_mismatch(candidate, brand_profile)
        assert mismatch is True

        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


class TestExternalDomainSimilarity:
    def test_suspicious_domain(self):
        from app.services.social_detection_service import SocialDetectionService
        from app.models import SocialCandidate, PlatformEnum, SourceTypeEnum
        from app.services.brand_intelligence_client import BrandProfile
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.database import Base

        engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        brand_profile = BrandProfile(
            brand_id="KAMPUSVC",
            name="KampusVC",
            official_domain="kampus.vc",
        )
        candidate = SocialCandidate(
            candidate_id="DEMO-DOMAIN-001",
            brand_id="KAMPUSVC",
            platform=PlatformEnum.INSTAGRAM,
            username="kampusvc_suspicious",
            display_name="KampusVC Suspicious",
            profile_url="https://instagram.com/kampusvc_suspicious",
            bio="Suspicious account",
            profile_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            logo_image_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
            followers_count=100,
            following_count=50,
            verification_status="none",
            external_links=["https://kampus-vc-login.com", "https://kampusvc-support.io"],
            contact_information={},
            collection_source=SourceTypeEnum.DEMO,
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        service = SocialDetectionService(db)
        similarity = service._calculate_external_domain_similarity(candidate, brand_profile)
        assert similarity is not None
        assert similarity < 50

        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
