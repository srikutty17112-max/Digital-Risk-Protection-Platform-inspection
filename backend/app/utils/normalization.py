import re
from typing import Optional, List
from urllib.parse import urlparse


def normalize_username(username: Optional[str]) -> str:
    if not username:
        return ""
    normalized = username.lower().strip()
    normalized = re.sub(r"[^a-z0-9]", "", normalized)
    return normalized


def normalize_display_name(display_name: Optional[str]) -> str:
    if not display_name:
        return ""
    normalized = display_name.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"[^\w\s]", "", normalized)
    return normalized


def normalize_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        parsed = urlparse(url.strip())
        normalized = parsed.netloc.lower().replace("www.", "")
        if parsed.path and parsed.path != "/":
            normalized += parsed.path.rstrip("/")
        return normalized
    except Exception:
        return url.strip().lower()


def normalize_domain(domain: Optional[str]) -> Optional[str]:
    if not domain:
        return None
    domain = domain.lower().strip()
    domain = domain.replace("www.", "")
    domain = domain.replace("http://", "").replace("https://", "")
    domain = domain.split("/")[0]
    return domain


def normalize_bio(bio: Optional[str]) -> str:
    if not bio:
        return ""
    normalized = bio.lower().strip()
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(r"[^\w\s@.#-]", " ", normalized)
    return normalized


def normalize_keywords(keywords: Optional[List[str]]) -> List[str]:
    if not keywords:
        return []
    normalized = []
    for kw in keywords:
        if kw:
            n = kw.lower().strip()
            n = re.sub(r"[^\w\s-]", "", n)
            if n:
                normalized.append(n)
    return list(set(normalized))


def normalize_aliases(aliases: Optional[List[str]]) -> List[str]:
    if not aliases:
        return []
    normalized = []
    for alias in aliases:
        if alias:
            n = alias.lower().strip()
            n = re.sub(r"[^\w\s.-]", "", n)
            n = re.sub(r"\s+", " ", n)
            if n:
                normalized.append(n)
    return list(set(normalized))


def extract_domain_from_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    try:
        parsed = urlparse(url.strip())
        return parsed.netloc.lower().replace("www.", "")
    except Exception:
        return None


def extract_domains_from_urls(urls: Optional[List[str]]) -> List[str]:
    if not urls:
        return []
    domains = []
    for url in urls:
        domain = extract_domain_from_url(url)
        if domain:
            domains.append(domain)
    return list(set(domains))


def extract_email_domain(email: Optional[str]) -> Optional[str]:
    if not email or "@" not in email:
        return None
    return email.split("@")[-1].lower().strip()


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    return digits if digits else None


class NormalizedCandidate:
    def __init__(
        self,
        candidate_id: str,
        brand_id: str,
        platform: str,
        username: Optional[str] = None,
        display_name: Optional[str] = None,
        profile_url: Optional[str] = None,
        bio: Optional[str] = None,
        profile_image_url: Optional[str] = None,
        logo_image_url: Optional[str] = None,
        followers_count: Optional[int] = None,
        following_count: Optional[int] = None,
        verification_status: Optional[str] = None,
        external_links: Optional[List[str]] = None,
        contact_information: Optional[dict] = None,
        collection_source: str = "DEMO",
        collected_at: Optional[str] = None,
    ):
        self.candidate_id = candidate_id
        self.brand_id = brand_id
        self.platform = platform

        self.username_original = username
        self.username_normalized = normalize_username(username)

        self.display_name_original = display_name
        self.display_name_normalized = normalize_display_name(display_name)

        self.profile_url_original = profile_url
        self.profile_url_normalized = normalize_url(profile_url)

        self.bio_original = bio
        self.bio_normalized = normalize_bio(bio)

        self.profile_image_url_original = profile_image_url
        self.logo_image_url_original = logo_image_url

        self.followers_count = followers_count
        self.following_count = following_count
        self.verification_status = verification_status

        self.external_links_original = external_links or []
        self.external_domains = extract_domains_from_urls(self.external_links_original)

        self.contact_information_original = contact_information or {}
        self.contact_email_domain = None
        self.contact_phone_normalized = None
        if contact_information:
            email = contact_information.get("email")
            if email:
                self.contact_email_domain = extract_email_domain(email)
            phone = contact_information.get("phone")
            if phone:
                self.contact_phone_normalized = normalize_phone(phone)

        self.collection_source = collection_source
        self.collected_at = collected_at

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "brand_id": self.brand_id,
            "platform": self.platform,
            "username_original": self.username_original,
            "username_normalized": self.username_normalized,
            "display_name_original": self.display_name_original,
            "display_name_normalized": self.display_name_normalized,
            "profile_url_original": self.profile_url_original,
            "profile_url_normalized": self.profile_url_normalized,
            "bio_original": self.bio_original,
            "bio_normalized": self.bio_normalized,
            "profile_image_url": self.profile_image_url_original,
            "logo_image_url": self.logo_image_url_original,
            "followers_count": self.followers_count,
            "following_count": self.following_count,
            "verification_status": self.verification_status,
            "external_links": self.external_links_original,
            "external_domains": self.external_domains,
            "contact_information": self.contact_information_original,
            "contact_email_domain": self.contact_email_domain,
            "contact_phone_normalized": self.contact_phone_normalized,
            "collection_source": self.collection_source,
            "collected_at": self.collected_at,
        }