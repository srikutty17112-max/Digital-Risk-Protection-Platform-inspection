from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from app.schemas_app import AppCandidateCreate
import json


@dataclass
class RawAppData:
    app_name: str
    store: str
    platform: str
    app_url: Optional[str] = None
    package_id: Optional[str] = None
    bundle_id: Optional[str] = None
    developer_name: Optional[str] = None
    developer_website: Optional[str] = None
    developer_email: Optional[str] = None
    app_icon_url: Optional[str] = None
    app_description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    download_count: Optional[int] = None
    external_links: List[str] = None
    raw_data: Dict[str, Any] = None

    def __post_init__(self):
        if self.external_links is None:
            self.external_links = []
        if self.raw_data is None:
            self.raw_data = {}


class AppStoreSourceAdapter(ABC):
    SOURCE_TYPE: str = "BASE"
    PLATFORM: str = "unknown"

    @abstractmethod
    def collect_candidates(self, brand_name: str, keywords: List[str], official_apps: List[Dict]) -> List[RawAppData]:
        pass

    def normalize_candidate(self, raw: RawAppData, brand_id: int, scan_job_id: int) -> AppCandidateCreate:
        normalized_name = self._normalize_app_name(raw.app_name)
        return AppCandidateCreate(
            brand_id=brand_id,
            scan_job_id=scan_job_id,
            app_name=raw.app_name,
            normalized_app_name=normalized_name,
            store=self.SOURCE_TYPE,
            platform=self.PLATFORM,
            app_url=raw.app_url,
            package_id=raw.package_id,
            bundle_id=raw.bundle_id,
            developer_name=raw.developer_name,
            developer_website=raw.developer_website,
            developer_email=raw.developer_email,
            app_icon_url=raw.app_icon_url,
            app_description=raw.app_description,
            short_description=raw.short_description,
            category=raw.category,
            version=raw.version,
            rating=raw.rating,
            review_count=raw.review_count,
            download_count=raw.download_count,
            external_links=raw.external_links or [],
            collection_source=self.SOURCE_TYPE,
        )

    def _normalize_app_name(self, name: str) -> str:
        import re
        name = name.lower().strip()
        name = re.sub(r'[^\w\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name


class DemoAppStoreAdapter(AppStoreSourceAdapter):
    SOURCE_TYPE = "DEMO"
    PLATFORM = "android"

    def __init__(self):
        self.demo_data = self._load_demo_data()

    def _load_demo_data(self) -> List[RawAppData]:
        official_icon = "https://via.placeholder.com/80x80/1a56db/ffffff?text=SB"
        official_icon_business = "https://via.placeholder.com/80x80/0d9488/ffffff?text=SB"
        lookalike_icon = "https://via.placeholder.com/80x80/1a56db/ffffff?text=SBN"
        lookalike_icon_tools = "https://via.placeholder.com/80x80/1a56db/ffffff?text=SBT"
        lookalike_icon_helper = "https://via.placeholder.com/80x80/1a56db/ffffff?text=SBH"
        lookalike_icon_rewards = "https://via.placeholder.com/80x80/1a56db/ffffff?text=SBR"
        return [
            # 1. Official mobile app (exact package match) -> OFFICIAL
            RawAppData(
                app_name="SecureBank Mobile",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.securebank.mobile",
                package_id="com.securebank.mobile",
                bundle_id=None,
                developer_name="SecureBank Financial Services Inc.",
                developer_website="https://securebank.com",
                developer_email="support@securebank.com",
                app_icon_url=official_icon,
                app_description="Official mobile banking app for SecureBank customers. Manage accounts, transfer funds, and monitor transactions securely.",
                short_description="Official mobile banking",
                category="Finance",
                version="3.2.1",
                rating=4.7,
                review_count=125000,
                download_count=5000000,
                external_links=["https://securebank.com"],
                raw_data={"source": "DEMO", "is_official": True}
            ),
            # 2. Official business app (exact package match) -> OFFICIAL
            RawAppData(
                app_name="SecureBank Business",
                store="DEMO",
                platform="ios",
                app_url="https://apps.apple.com/app/securebank-business/id123456789",
                package_id=None,
                bundle_id="com.securebank.business",
                developer_name="SecureBank Financial Services Inc.",
                developer_website="https://securebank.com",
                developer_email="support@securebank.com",
                app_icon_url=official_icon_business,
                app_description="Business banking solution for SecureBank commercial clients. Multi-user access, approval workflows, and advanced reporting.",
                short_description="Business banking",
                category="Finance",
                version="2.1.0",
                rating=4.5,
                review_count=8900,
                download_count=500000,
                external_links=["https://securebank.com"],
                raw_data={"source": "DEMO", "is_official": True}
            ),
            # 3. Character swap -> LIKELY_IMPERSONATION
            RawAppData(
                app_name="SecureBnak",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.securebnak.app",
                package_id="com.securebnak.app",
                bundle_id=None,
                developer_name="SecureBnak Dev Team",
                developer_website="https://securebnak.com",
                developer_email="support@securebnak.com",
                app_icon_url=lookalike_icon,
                app_description="SecureBank mobile banking app. Manage accounts, transfer funds, and pay securely.",
                short_description="Mobile banking",
                category="Finance",
                version="1.0.0",
                rating=3.2,
                review_count=120,
                download_count=5000,
                external_links=["https://securebnak.com"],
                raw_data={"source": "DEMO", "is_official": False, "lookalike": True, "pattern": "CHARACTER_SWAP"}
            ),
            # 4. Added word "Tools" -> LIKELY_IMPERSONATION
            RawAppData(
                app_name="SecureBank Tools",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.fake.securebank.tools",
                package_id="com.fake.securebank.tools",
                bundle_id=None,
                developer_name="Unknown Apps Studio",
                developer_website="https://unknownapps.example.com",
                developer_email="contact@unknownapps.example.com",
                app_icon_url=lookalike_icon,
                app_description="SecureBank tools and utilities for banking customers. Account helpers and security tools.",
                short_description="Banking tools",
                category="Tools",
                version="1.2.0",
                rating=3.5,
                review_count=340,
                download_count=10000,
                external_links=["https://unknownapps.example.com"],
                raw_data={"source": "DEMO", "is_official": False, "lookalike": True, "pattern": "ADDED_WORD"}
            ),
            # 5. Added word "Helper", possible publisher match -> SUSPICIOUS
            RawAppData(
                app_name="SecureBank Helper",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.securebank.helper",
                package_id=None,
                bundle_id=None,
                developer_name="SecureBank",
                developer_website=None,
                developer_email=None,
                app_icon_url=lookalike_icon_helper,
                app_description="Helper app for SecureBank customers with account tools and support contacts.",
                short_description="Account helper",
                category="Finance",
                version="1.0.5",
                rating=4.1,
                review_count=890,
                download_count=50000,
                external_links=[],
                raw_data={"source": "DEMO", "is_official": False, "lookalike": True, "pattern": "ADDED_WORD"}
            ),
            # 6. Added word "Rewards" -> LIKELY_IMPERSONATION
            RawAppData(
                app_name="SecureBank Rewards",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.fake.securebank.rewards",
                package_id="com.fake.securebank.rewards",
                bundle_id=None,
                developer_name="Rewards Apps Ltd",
                developer_website="https://rewardsapps.example.com",
                developer_email="info@rewardsapps.example.com",
                app_icon_url=lookalike_icon,
                app_description="SecureBank rewards and cashback program. Earn points on every transaction.",
                short_description="Rewards program",
                category="Finance",
                version="2.0.0",
                rating=3.8,
                review_count=560,
                download_count=25000,
                external_links=["https://rewardsapps.example.com"],
                raw_data={"source": "DEMO", "is_official": False, "lookalike": True, "pattern": "ADDED_WORD"}
            ),
            # 7. Added word "Pro", possible publisher, same icon domain -> LIKELY_LEGITIMATE
            RawAppData(
                app_name="SecureBank Pro",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.securebank.pro",
                package_id=None,
                bundle_id=None,
                developer_name="SecureBank",
                developer_website="https://securebank.com",
                developer_email="support@securebank.com",
                app_icon_url=official_icon,
                app_description="SecureBank Pro with advanced features for power users.",
                short_description="Pro features",
                category="Finance",
                version="1.0.0",
                rating=4.3,
                review_count=450,
                download_count=12000,
                external_links=["https://securebank.com"],
                raw_data={"source": "DEMO", "is_official": False, "variant": "pro"}
            ),
            # 8. Unrelated app -> LIKELY_LEGITIMATE
            RawAppData(
                app_name="Unrelated Productivity Suite",
                store="DEMO",
                platform="android",
                app_url="https://play.google.com/store/apps/details?id=com.unrelated.productivity",
                package_id=None,
                bundle_id=None,
                developer_name="Productivity Labs",
                developer_website=None,
                developer_email=None,
                app_icon_url="https://via.placeholder.com/80x80/6b7280/ffffff?text=UP",
                app_description="General productivity suite with notes, tasks, and calendar for professionals.",
                short_description="Productivity suite",
                category="Productivity",
                version="4.1.2",
                rating=4.4,
                review_count=8900,
                download_count=300000,
                external_links=["https://productivitylabs.example.com"],
                raw_data={"source": "DEMO", "is_official": False, "unrelated": True}
            ),
        ]

    def collect_candidates(self, brand_name: str, keywords: List[str], official_apps: List[Dict]) -> List[RawAppData]:
        return self.demo_data.copy()


class GooglePlayStoreAdapter(AppStoreSourceAdapter):
    SOURCE_TYPE = "GOOGLE_PLAY"
    PLATFORM = "android"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)

    def collect_candidates(self, brand_name: str, keywords: List[str], official_apps: List[Dict]) -> List[RawAppData]:
        if not self.enabled:
            raise RuntimeError("Google Play adapter not configured. Set GOOGLE_PLAY_API_KEY.")
        return []


class AppleAppStoreAdapter(AppStoreSourceAdapter):
    SOURCE_TYPE = "APPLE_APP_STORE"
    PLATFORM = "ios"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.enabled = bool(api_key)

    def collect_candidates(self, brand_name: str, keywords: List[str], official_apps: List[Dict]) -> List[RawAppData]:
        if not self.enabled:
            raise RuntimeError("Apple App Store adapter not configured. Set APP_STORE_API_KEY.")
        return []


class ImportedAppStoreAdapter(AppStoreSourceAdapter):
    SOURCE_TYPE = "IMPORTED"
    PLATFORM = "unknown"

    def __init__(self, imported_data: List[Dict]):
        self.imported_data = imported_data

    def collect_candidates(self, brand_name: str, keywords: List[str], official_apps: List[Dict]) -> List[RawAppData]:
        candidates = []
        for item in self.imported_data:
            candidates.append(RawAppData(
                app_name=item.get("app_name", ""),
                store=self.SOURCE_TYPE,
                platform=item.get("platform", "unknown"),
                app_url=item.get("app_url"),
                package_id=item.get("package_id"),
                bundle_id=item.get("bundle_id"),
                developer_name=item.get("developer_name"),
                developer_website=item.get("developer_website"),
                developer_email=item.get("developer_email"),
                app_icon_url=item.get("app_icon_url"),
                app_description=item.get("app_description"),
                short_description=item.get("short_description"),
                category=item.get("category"),
                version=item.get("version"),
                rating=item.get("rating"),
                review_count=item.get("review_count"),
                download_count=item.get("download_count"),
                external_links=item.get("external_links", []),
                raw_data=item.get("raw_data", {}),
            ))
        return candidates


def get_source_adapter(source_type: str, **kwargs) -> AppStoreSourceAdapter:
    source_type = source_type.upper()
    if source_type == "DEMO":
        return DemoAppStoreAdapter()
    elif source_type == "GOOGLE_PLAY":
        return GooglePlayStoreAdapter(kwargs.get("api_key"))
    elif source_type == "APPLE_APP_STORE":
        return AppleAppStoreAdapter(kwargs.get("api_key"))
    elif source_type == "IMPORTED":
        return ImportedAppStoreAdapter(kwargs.get("imported_data", []))
    elif source_type == "MOCK":
        return DemoAppStoreAdapter()
    else:
        raise ValueError(f"Unknown source type: {source_type}")
