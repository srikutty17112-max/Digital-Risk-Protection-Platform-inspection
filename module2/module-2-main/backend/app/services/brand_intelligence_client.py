import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import httpx
from app.config import settings

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
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 10.0,
    ):
        self.base_url = base_url or settings.MODULE1_API_BASE_URL
        self.api_key = api_key or settings.MODULE1_API_KEY
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._available: Optional[bool] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def check_availability(self) -> bool:
        if self._available is not None:
            return self._available

        try:
            client = await self._get_client()
            response = await client.get("/health", timeout=5.0)
            self._available = response.status_code == 200
            if self._available:
                logger.info("Module 1 (Brand Intelligence) is available")
            else:
                logger.warning(f"Module 1 health check failed: {response.status_code}")
        except Exception as e:
            logger.warning(f"Module 1 unavailable: {e}")
            self._available = False

        return self._available

    async def get_brand_profile(self, brand_id: str) -> Optional[BrandProfile]:
        if not await self.check_availability():
            logger.info(f"Module 1 unavailable, returning demo data for brand {brand_id}")
            return self._get_demo_brand_profile(brand_id)

        try:
            client = await self._get_client()
            response = await client.get(f"/api/brands/{brand_id}", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
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
            else:
                logger.warning(f"Module 1 returned {response.status_code} for brand {brand_id}")
        except Exception as e:
            logger.error(f"Error fetching brand profile from Module 1: {e}")

        return self._get_demo_brand_profile(brand_id)

    async def get_official_social_accounts(self, brand_id: str) -> List[OfficialSocialAccount]:
        profile = await self.get_brand_profile(brand_id)
        if not profile or not profile.official_social_accounts:
            return []

        accounts = []
        for acc in profile.official_social_accounts:
            accounts.append(
                OfficialSocialAccount(
                    platform=acc.get("platform", ""),
                    username=acc.get("username", ""),
                    display_name=acc.get("display_name"),
                    profile_url=acc.get("profile_url"),
                    verified=acc.get("verified", False),
                    asset_id=acc.get("asset_id"),
                )
            )
        return accounts

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
        if brand_id.upper() == "SECUREBANK":
            return BrandProfile(
                brand_id="SECUREBANK",
                name="SecureBank",
                official_website="https://securebank.com",
                official_domain="securebank.com",
                official_social_accounts=[
                    {
                        "platform": "twitter",
                        "username": "securebank",
                        "display_name": "SecureBank",
                        "profile_url": "https://twitter.com/securebank",
                        "verified": True,
                        "asset_id": "ASSET-SECUREBANK-TWITTER-001",
                    },
                    {
                        "platform": "linkedin",
                        "username": "securebank",
                        "display_name": "SecureBank",
                        "profile_url": "https://linkedin.com/company/securebank",
                        "verified": True,
                        "asset_id": "ASSET-SECUREBANK-LINKEDIN-001",
                    },
                    {
                        "platform": "facebook",
                        "username": "securebank",
                        "display_name": "SecureBank",
                        "profile_url": "https://facebook.com/securebank",
                        "verified": True,
                        "asset_id": "ASSET-SECUREBANK-FACEBOOK-001",
                    },
                    {
                        "platform": "instagram",
                        "username": "securebank",
                        "display_name": "SecureBank",
                        "profile_url": "https://instagram.com/securebank",
                        "verified": True,
                        "asset_id": "ASSET-SECUREBANK-INSTAGRAM-001",
                    },
                    {
                        "platform": "youtube",
                        "username": "securebank",
                        "display_name": "SecureBank",
                        "profile_url": "https://youtube.com/@securebank",
                        "verified": True,
                        "asset_id": "ASSET-SECUREBANK-YOUTUBE-001",
                    },
                ],
                logo_url="https://via.placeholder.com/120x120/1a56db/ffffff?text=SB",
                brand_keywords=["banking", "fintech", "digital banking", "secure payments", "financial services"],
                aliases=["Secure Bank", "SecureBank Financial", "SBFS"],
                registered_names=["SecureBank Financial Services Inc.", "SecureBank"],
                contact_email="support@securebank.com",
                contact_phone="+1-555-0100",
                description="SecureBank is a leading digital banking platform providing secure financial services to millions of customers worldwide.",
            )
        elif brand_id.upper() == "KAMPUSVC":
            return BrandProfile(
                brand_id="KAMPUSVC",
                name="KampusVC",
                official_website="https://kampus.vc",
                official_domain="kampus.vc",
                official_social_accounts=[
                    {
                        "platform": "instagram",
                        "username": "kampusvc",
                        "display_name": "KampusVC",
                        "profile_url": "https://instagram.com/kampusvc",
                        "verified": True,
                        "asset_id": "ASSET-KAMPUSVC-INSTA-001",
                    },
                    {
                        "platform": "twitter",
                        "username": "kampusvc",
                        "display_name": "KampusVC",
                        "profile_url": "https://twitter.com/kampusvc",
                        "verified": True,
                        "asset_id": "ASSET-KAMPUSVC-TWITTER-001",
                    },
                    {
                        "platform": "linkedin",
                        "username": "kampusvc",
                        "display_name": "KampusVC",
                        "profile_url": "https://linkedin.com/company/kampusvc",
                        "verified": True,
                        "asset_id": "ASSET-KAMPUSVC-LINKEDIN-001",
                    },
                ],
                logo_url="https://demo-assets.brandshield.io/kampusvc/logo.png",
                brand_keywords=["venture capital", "student startups", "funding", "founders", "university"],
                aliases=["Kampus VC", "Kampus.VC", "KV"],
                registered_names=["KampusVC Inc.", "Kampus Venture Capital"],
                contact_email="hello@kampus.vc",
                contact_phone="+1-555-0100",
                description="Venture capital fund investing in student-founded startups",
            )
        else:
            return BrandProfile(
                brand_id=brand_id,
                name=brand_id,
                official_website=f"https://{brand_id.lower()}.com",
                official_domain=f"{brand_id.lower()}.com",
                official_social_accounts=[
                    {
                        "platform": "instagram",
                        "username": brand_id.lower(),
                        "display_name": brand_id,
                        "profile_url": f"https://instagram.com/{brand_id.lower()}",
                        "verified": True,
                        "asset_id": f"ASSET-{brand_id}-INSTA-001",
                    }
                ],
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