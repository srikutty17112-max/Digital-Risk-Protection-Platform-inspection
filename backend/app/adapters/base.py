from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from app.schemas import PlatformEnum, SourceTypeEnum


@dataclass
class SocialCandidateData:
    candidate_id: str
    brand_id: str
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
    collection_source: SourceTypeEnum = SourceTypeEnum.DEMO
    collected_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "brand_id": self.brand_id,
            "platform": self.platform.value,
            "username": self.username,
            "display_name": self.display_name,
            "profile_url": self.profile_url,
            "bio": self.bio,
            "profile_image_url": self.profile_image_url,
            "logo_image_url": self.logo_image_url,
            "followers_count": self.followers_count,
            "following_count": self.following_count,
            "verification_status": self.verification_status,
            "external_links": self.external_links,
            "contact_information": self.contact_information,
            "collection_source": self.collection_source.value,
            "collected_at": self.collected_at or datetime.utcnow(),
        }


class SocialSourceAdapter(ABC):
    def __init__(self, source_type: SourceTypeEnum):
        self.source_type = source_type

    @abstractmethod
    async def collect_candidates(
        self,
        brand_id: str,
        brand_name: str,
        official_usernames: List[str],
        platforms: Optional[List[PlatformEnum]] = None,
        limit_per_platform: int = 50,
    ) -> List[SocialCandidateData]:
        pass

    @abstractmethod
    async def get_candidate_details(
        self,
        candidate_id: str,
        platform: PlatformEnum,
    ) -> Optional[SocialCandidateData]:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def get_supported_platforms(self) -> List[PlatformEnum]:
        pass

    def get_source_type(self) -> SourceTypeEnum:
        return self.source_type