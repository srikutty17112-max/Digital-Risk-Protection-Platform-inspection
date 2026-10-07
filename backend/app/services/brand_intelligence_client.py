import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from app.services.brand.registry import brand_registry

logger = logging.getLogger(__name__)


@dataclass
class BrandProfile:
    brand_id: str
    name: str
    official_website: Optional[str] = None
    official_domain: Optional[str] = None
    official_social_accounts: Optional[List[Dict[str, Any]]] = None
    logo_url: Optional[str] = None
    brand_keywords: Optional[List[str]] = None
    aliases: Optional[List[str]] = None
    registered_names: Optional[List[str]] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    description: Optional[str] = None


@dataclass
class OfficialSocialAccount:
    platform: str
    username: str
    display_name: Optional[str] = None
    profile_url: Optional[str] = None
    verified: bool = False
    asset_id: Optional[str] = None


class BrandIntelligenceClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: float = 10.0):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout

    async def check_availability(self) -> bool:
        return True

    async def get_brand_profile(self, brand_id: str) -> Optional[BrandProfile]:
        data = brand_registry.get_brand(brand_id)
        if not data:
            return self._get_demo_brand_profile(brand_id)
        return BrandProfile(
            brand_id=data.get("brand_id", brand_id),
            name=data.get("name", ""),
            official_website=data.get("official_website"),
            official_domain=data.get("official_domain"),
            official_social_accounts=data.get("official_social_accounts", []),
            logo_url=data.get("logo_url"),
            brand_keywords=data.get("brand_keywords", []),
            aliases=data.get("aliases", []),
            registered_names=data.get("registered_names", []),
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
            description=data.get("description"),
        )

    async def get_official_social_accounts(self, brand_id: str) -> List[OfficialSocialAccount]:
        profile = await self.get_brand_profile(brand_id)
        if not profile or not profile.official_social_accounts:
            return []
        return [
            OfficialSocialAccount(
                platform=acc.get("platform", ""),
                username=acc.get("username", ""),
                display_name=acc.get("display_name"),
                profile_url=acc.get("profile_url"),
                verified=acc.get("verified", False),
                asset_id=acc.get("asset_id"),
            )
            for acc in profile.official_social_accounts
        ]

    async def get_official_logo_url(self, brand_id: str) -> Optional[str]:
        profile = await self.get_brand_profile(brand_id)
        return profile.logo_url if profile else None

    async def get_brand_keywords(self, brand_id: str) -> List[str]:
        profile = await self.get_brand_profile(brand_id)
        return profile.brand_keywords if profile else []

    async def get_brand_aliases(self, brand_id: str) -> List[str]:
        profile = await self.get_brand_profile(brand_id)
        return profile.aliases if profile else []

    async def get_official_domain(self, brand_id: str) -> Optional[str]:
        profile = await self.get_brand_profile(brand_id)
        return profile.official_domain if profile else None

    def _get_demo_brand_profile(self, brand_id: str) -> BrandProfile:
        data = brand_registry.get_brand(brand_id)
        if data:
            return BrandProfile(
                brand_id=data.get("brand_id", brand_id),
                name=data.get("name", brand_id),
                official_website=data.get("official_website", f"https://{brand_id.lower()}.com"),
                official_domain=data.get("official_domain", f"{brand_id.lower()}.com"),
                official_social_accounts=data.get("official_social_accounts", []),
                logo_url=data.get("logo_url", f"https://demo-assets.brandshield.io/{brand_id.lower()}/logo.png"),
                brand_keywords=data.get("brand_keywords", [brand_id.lower(), "technology", "innovation"]),
                aliases=data.get("aliases", [brand_id]),
                registered_names=data.get("registered_names", [f"{brand_id} Inc."]),
                contact_email=data.get("contact_email", f"hello@{brand_id.lower()}.com"),
                contact_phone=data.get("contact_phone"),
                description=data.get("description", f"Official brand: {brand_id}"),
            )
        return BrandProfile(
            brand_id=brand_id,
            name=brand_id,
            official_website=f"https://{brand_id.lower()}.com",
            official_domain=f"{brand_id.lower()}.com",
            official_social_accounts=[],
            logo_url=f"https://demo-assets.brandshield.io/{brand_id.lower()}/logo.png",
            brand_keywords=[brand_id.lower(), "technology", "innovation"],
            aliases=[brand_id],
            registered_names=[f"{brand_id} Inc."],
            contact_email=f"hello@{brand_id.lower()}.com",
            description=f"Official brand: {brand_id}",
        )


_brand_intelligence_client: Optional[BrandIntelligenceClient] = None


def get_brand_intelligence_client() -> BrandIntelligenceClient:
    global _brand_intelligence_client
    if _brand_intelligence_client is None:
        _brand_intelligence_client = BrandIntelligenceClient()
    return _brand_intelligence_client
