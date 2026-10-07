from typing import List, Dict, Any

BRAND_ID = "SECUREBANK"

BRAND_PROFILE: Dict[str, Any] = {
    "brand_id": BRAND_ID,
    "name": "SecureBank",
    "company_name": "SecureBank Financial Services Inc.",
    "official_website": "https://securebank.com",
    "official_domain": "securebank.com",
    "description": "SecureBank is a leading digital banking platform providing secure financial services to millions of customers worldwide. Founded in 2010, we pioneered zero-trust architecture in consumer banking.",
    "brand_keywords": ["banking", "fintech", "digital banking", "secure payments", "financial services"],
    "keywords": ["banking", "fintech", "digital banking", "secure payments", "financial services"],
    "aliases": ["Secure Bank", "SecureBank Financial", "SBFS"],
    "registered_names": ["SecureBank Financial Services Inc.", "SecureBank"],
    "logo_url": "https://via.placeholder.com/120x120/1a56db/ffffff?text=SB",
    "contact_email": "support@securebank.com",
    "contact_phone": "+1-555-0100",
}

OFFICIAL_SOCIAL_ACCOUNTS: List[Dict[str, Any]] = [
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
]

OFFICIAL_MOBILE_APPS: List[Dict[str, Any]] = [
    {
        "app_id": "app-1",
        "name": "SecureBank Mobile",
        "package_id": "com.securebank.mobile",
        "bundle_id": None,
        "developer": "SecureBank Financial Services Inc.",
        "store_url": "https://play.google.com/store/apps/details?id=com.securebank.mobile",
        "store": "GOOGLE_PLAY",
        "platform": "android",
        "logo_url": "https://via.placeholder.com/80x80/1a56db/ffffff?text=SB",
        "description": "Official mobile banking app for SecureBank customers. Manage accounts, transfer funds, and monitor transactions securely.",
    },
    {
        "app_id": "app-2",
        "name": "SecureBank Business",
        "package_id": "com.securebank.business",
        "bundle_id": None,
        "developer": "SecureBank Financial Services Inc.",
        "store_url": "https://apps.apple.com/app/securebank-business/id123456789",
        "store": "APPLE_APP_STORE",
        "platform": "ios",
        "logo_url": "https://via.placeholder.com/80x80/0d9488/ffffff?text=SB",
        "description": "Business banking solution for SecureBank commercial clients. Multi-user access, approval workflows, and advanced reporting.",
    },
]

BRAND_FINGERPRINT: Dict[str, Any] = {
    "officialBrandName": "SecureBank",
    "normalizedName": "securebank",
    "similarityEngine": "Levenshtein + Phonetic + Semantic Embedding",
    "candidateName": "SecureBank",
    "similarityScore": 100,
}


class BrandRegistryService:
    def get_brand(self, brand_id: str) -> Dict[str, Any]:
        if brand_id.upper() != BRAND_ID:
            return {}
        profile = dict(BRAND_PROFILE)
        profile["official_social_accounts"] = OFFICIAL_SOCIAL_ACCOUNTS
        profile["official_mobile_apps"] = OFFICIAL_MOBILE_APPS
        profile["brand_fingerprint"] = BRAND_FINGERPRINT
        return profile

    def list_brands(self) -> List[Dict[str, Any]]:
        return [self.get_brand(BRAND_ID)]


brand_registry = BrandRegistryService()
