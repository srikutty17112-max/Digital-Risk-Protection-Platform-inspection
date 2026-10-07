from typing import List, Optional, Dict, Any
from datetime import datetime
from app.adapters.base import SocialSourceAdapter, SocialCandidateData
from app.schemas import PlatformEnum, SourceTypeEnum


class DemoSocialAdapter(SocialSourceAdapter):
    def __init__(self):
        super().__init__(SourceTypeEnum.DEMO)
        self._demo_data = self._initialize_demo_data()

    def _initialize_demo_data(self) -> Dict[str, List[SocialCandidateData]]:
        now = datetime.utcnow()
        official_logo = "https://via.placeholder.com/120x120/1a56db/ffffff?text=SB"
        similar_logo = "https://via.placeholder.com/120x120/1a56db/ffffff?text=SB"
        return {
            "SECUREBANK": [
                # 1. Official account (exact username + profile_url match) -> OFFICIAL
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-TWITTER-001",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.X_TWITTER,
                    username="securebank",
                    display_name="SecureBank",
                    profile_url="https://twitter.com/securebank",
                    bio="SecureBank | Digital banking for millions. Secure payments, fintech innovation. Official account.",
                    profile_image_url=official_logo,
                    logo_image_url=official_logo,
                    followers_count=250000,
                    following_count=342,
                    verification_status="verified",
                    external_links=["https://securebank.com", "https://linkedin.com/company/securebank"],
                    contact_information={"email": "support@securebank.com", "website": "https://securebank.com"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 2. Character swap -> HIGH_RISK_IMPERSONATION
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-INSTA-002",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.INSTAGRAM,
                    username="securebnak",
                    display_name="SecureBnak",
                    profile_url="https://instagram.com/securebnak",
                    bio="SecureBank digital banking platform. Manage accounts, transfer funds, secure payments.",
                    profile_image_url=similar_logo,
                    logo_image_url=similar_logo,
                    followers_count=3420,
                    following_count=1200,
                    verification_status="none",
                    external_links=["https://securebnak.com", "https://securebnak-login.com"],
                    contact_information={"email": "support@securebnak.com", "phone": "+1-555-0199"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 3. Added word "official" -> HIGH_RISK_IMPERSONATION
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-INSTA-003",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.INSTAGRAM,
                    username="securebank_official",
                    display_name="SecureBank Official",
                    profile_url="https://instagram.com/securebank_official",
                    bio="The official SecureBank application. Digital banking, secure payments, financial services.",
                    profile_image_url=similar_logo,
                    logo_image_url=similar_logo,
                    followers_count=8900,
                    following_count=200,
                    verification_status="none",
                    external_links=["https://securebank-official.com", "https://securebank-verify.com"],
                    contact_information={"email": "contact@securebank-official.com", "phone": "+1-555-0201"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 4. Added word "support" -> LIKELY_IMPERSONATION
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-FB-004",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.FACEBOOK,
                    username="securebank_support",
                    display_name="SecureBank Support",
                    profile_url="https://facebook.com/securebank_support",
                    bio="Customer support for SecureBank. Help with account issues, verification, and banking.",
                    profile_image_url=similar_logo,
                    logo_image_url=similar_logo,
                    followers_count=1200,
                    following_count=50,
                    verification_status="none",
                    external_links=["https://support-center.io"],
                    contact_information={},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 5. Spacing change -> LIKELY_IMPERSONATION
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-LI-005",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.LINKEDIN,
                    username="secure bank",
                    display_name="Secure Bank",
                    profile_url="https://linkedin.com/company/secure-bank",
                    bio="Secure Bank - digital banking and secure payments for modern customers.",
                    profile_image_url=similar_logo,
                    logo_image_url=similar_logo,
                    followers_count=5600,
                    following_count=200,
                    verification_status="none",
                    external_links=["https://secure-bank.co"],
                    contact_information={"email": "info@secure-bank.co"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 6. Concatenated (no separator) -> SUSPICIOUS
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-YT-006",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.YOUTUBE,
                    username="securebankofficial",
                    display_name="SecureBankOfficial",
                    profile_url="https://youtube.com/@securebankofficial",
                    bio="SecureBankOfficial channel for banking updates.",
                    profile_image_url=similar_logo,
                    logo_image_url=similar_logo,
                    followers_count=450,
                    following_count=10,
                    verification_status="none",
                    external_links=[],
                    contact_information={},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                # 7. Unrelated company -> LIKELY_LEGITIMATE (false-positive protection)
                SocialCandidateData(
                    candidate_id="DEMO-SECUREBANK-ZOOM-007",
                    brand_id="SECUREBANK",
                    platform=PlatformEnum.TIKTOK,
                    username="zoom",
                    display_name="Zoom",
                    profile_url="https://tiktok.com/@zoom",
                    bio="Video conferencing for modern teams. Host meetings, webinars, and team chat.",
                    profile_image_url="https://via.placeholder.com/120x120/6b7280/ffffff?text=ZM",
                    logo_image_url="https://via.placeholder.com/120x120/6b7280/ffffff?text=ZM",
                    followers_count=15000,
                    following_count=500,
                    verification_status="verified",
                    external_links=[],
                    contact_information={},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
            ],
            "DEFAULT": [
                SocialCandidateData(
                    candidate_id="DEMO-DEFAULT-INSTA-001",
                    brand_id="DEFAULT",
                    platform=PlatformEnum.INSTAGRAM,
                    username="brandofficial",
                    display_name="Brand Official",
                    profile_url="https://instagram.com/brandofficial",
                    bio="Official brand account",
                    profile_image_url="https://demo-assets.brandshield.io/default/logo.png",
                    logo_image_url="https://demo-assets.brandshield.io/default/logo.png",
                    followers_count=10000,
                    following_count=100,
                    verification_status="verified",
                    external_links=["https://brand.com"],
                    contact_information={"email": "hello@brand.com"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
                SocialCandidateData(
                    candidate_id="DEMO-DEFAULT-INSTA-002",
                    brand_id="DEFAULT",
                    platform=PlatformEnum.INSTAGRAM,
                    username="brandofficiall",
                    display_name="Brand Official Support",
                    profile_url="https://instagram.com/brandofficiall",
                    bio="Support account for Brand Official",
                    profile_image_url="https://demo-assets.brandshield.io/default/logo_similar.png",
                    logo_image_url="https://demo-assets.brandshield.io/default/logo_similar.png",
                    followers_count=1000,
                    following_count=200,
                    verification_status="none",
                    external_links=["https://brand-support.com"],
                    contact_information={"email": "support@brand-support.com"},
                    collection_source=SourceTypeEnum.DEMO,
                    collected_at=now,
                ),
            ],
        }

    async def collect_candidates(
        self,
        brand_id: str,
        brand_name: str,
        official_usernames: List[str],
        platforms: Optional[List[PlatformEnum]] = None,
        limit_per_platform: int = 50,
    ) -> List[SocialCandidateData]:
        candidates = self._demo_data.get(brand_id.upper(), self._demo_data["DEFAULT"])
        if platforms:
            candidates = [c for c in candidates if c.platform in platforms]
        return candidates[:limit_per_platform]

    async def get_candidate_details(
        self,
        candidate_id: str,
        platform: PlatformEnum,
    ) -> Optional[SocialCandidateData]:
        for candidates in self._demo_data.values():
            for candidate in candidates:
                if candidate.candidate_id == candidate_id and candidate.platform == platform:
                    return candidate
        return None

    def is_available(self) -> bool:
        return True

    def get_supported_platforms(self) -> List[PlatformEnum]:
        return [
            PlatformEnum.INSTAGRAM,
            PlatformEnum.FACEBOOK,
            PlatformEnum.X_TWITTER,
            PlatformEnum.LINKEDIN,
            PlatformEnum.YOUTUBE,
            PlatformEnum.TIKTOK,
        ]


class DatasetSocialAdapter(SocialSourceAdapter):
    def __init__(self, dataset_path: str):
        super().__init__(SourceTypeEnum.IMPORTED)
        self.dataset_path = dataset_path
        self._cached_data: List[SocialCandidateData] = []

    async def collect_candidates(
        self,
        brand_id: str,
        brand_name: str,
        official_usernames: List[str],
        platforms: Optional[List[PlatformEnum]] = None,
        limit_per_platform: int = 50,
    ) -> List[SocialCandidateData]:
        return []

    async def get_candidate_details(
        self,
        candidate_id: str,
        platform: PlatformEnum,
    ) -> Optional[SocialCandidateData]:
        return None

    def is_available(self) -> bool:
        return False

    def get_supported_platforms(self) -> List[PlatformEnum]:
        return []


def get_demo_adapter() -> DemoSocialAdapter:
    return DemoSocialAdapter()
