from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models import (
    SocialCandidate,
    SocialDetectionResult,
    SocialDetectionSignal,
    ThreatClassificationEnum,
    RiskLevelEnum,
    LookalikePatternEnum,
    OfficialMatchTypeEnum,
    ThreatStatusEnum,
)
from app.services.brand_intelligence_client import BrandProfile, OfficialSocialAccount
from app.utils import (
    calculate_name_similarity,
    detect_lookalike_pattern,
    compare_logo_with_official,
    calculate_risk_score,
    determine_risk_level,
    determine_classification,
    calculate_confidence,
    generate_reasons,
    assess_false_positive_risk,
    normalize_display_name,
    normalize_username,
    extract_domain_from_url,
    DEFAULT_WEIGHTS,
)
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class SocialDetectionService:
    def __init__(self, db: Session):
        self.db = db

    async def analyze_candidate(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
        official_accounts: List[OfficialSocialAccount],
    ) -> SocialDetectionResult:
        official_match = self._check_official_match(candidate, official_accounts)

        if official_match["is_official"]:
            return self._create_official_result(candidate, brand_profile, official_match)

        name_similarity = self._calculate_name_similarity(candidate, brand_profile)
        lookalike = self._detect_lookalike(candidate, brand_profile)
        logo_similarity = await self._calculate_logo_similarity(candidate, brand_profile)
        branding_similarity = self._calculate_branding_similarity(candidate, brand_profile)
        external_domain_similarity = self._calculate_external_domain_similarity(candidate, brand_profile)
        identifier_mismatch = self._check_identifier_mismatch(candidate, brand_profile)

        risk_score = calculate_risk_score(
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            external_domain_similarity=external_domain_similarity,
            official_mismatch=not official_match["is_official"],
            identifier_mismatch=identifier_mismatch,
            weights=DEFAULT_WEIGHTS,
        )

        risk_level = determine_risk_level(risk_score)

        is_false_positive, fp_reason = assess_false_positive_risk(
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            lookalike_detected=lookalike["detected"],
            official_keywords=brand_profile.brand_keywords or [],
            candidate_bio=candidate.bio,
        )

        if is_false_positive and risk_score < 60:
            risk_score = min(risk_score, 40)
            risk_level = determine_risk_level(risk_score)

        confidence = calculate_confidence(
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            external_domain_similarity=external_domain_similarity,
            has_profile_image=bool(candidate.profile_image_url),
            has_bio=bool(candidate.bio),
            has_external_links=bool(candidate.external_links),
            official_match_confidence=official_match["confidence"],
        )

        classification = determine_classification(
            risk_score=risk_score,
            risk_level=risk_level,
            is_official=False,
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            lookalike_detected=lookalike["detected"],
            external_domain_suspicious=external_domain_similarity is not None and external_domain_similarity < 50,
            confidence=confidence,
        )

        reasons = generate_reasons(
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            external_domain_similarity=external_domain_similarity,
            official_match=official_match,
            lookalike=lookalike,
            identifier_mismatch=identifier_mismatch,
            candidate_data={
                "verification_status": candidate.verification_status,
                "bio": candidate.bio,
                "external_links": candidate.external_links,
            },
        )

        if fp_reason:
            reasons.append(fp_reason)

        threat_id = f"SOCIAL-THREAT-{uuid.uuid4().hex[:8].upper()}"

        detection_result = SocialDetectionResult(
            threat_id=threat_id,
            candidate_id=candidate.id,
            brand_id=candidate.brand_id,
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            external_domain_similarity=external_domain_similarity,
            lookalike_detected=lookalike["detected"],
            lookalike_pattern=lookalike["pattern"],
            lookalike_similarity=lookalike["similarity"],
            lookalike_explanation=lookalike["explanation"],
            official_match_is_official=official_match["is_official"],
            official_match_asset_id=official_match["matched_asset_id"],
            official_match_type=official_match["match_type"],
            official_match_confidence=official_match["confidence"],
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            classification=classification,
            reasons=reasons,
            source_type=candidate.collection_source,
            collected_at=candidate.collected_at,
            status=ThreatStatusEnum.NEW,
        )

        self.db.add(detection_result)
        self.db.flush()

        signal = SocialDetectionSignal(
            result_id=detection_result.id,
            name_similarity=name_similarity,
            logo_similarity=logo_similarity,
            branding_similarity=branding_similarity,
            external_domain_similarity=external_domain_similarity,
            identifier_mismatch_score=1.0 if identifier_mismatch else 0.0,
            official_mismatch=not official_match["is_official"],
            raw_signals={
                "lookalike": lookalike,
                "official_match": official_match,
                "identifier_mismatch": identifier_mismatch,
            },
        )
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(detection_result)

        return detection_result

    def _check_official_match(
        self,
        candidate: SocialCandidate,
        official_accounts: List[OfficialSocialAccount],
    ) -> Dict[str, Any]:
        candidate_username_norm = normalize_username(candidate.username)
        candidate_display_norm = normalize_display_name(candidate.display_name)

        for acc in official_accounts:
            official_username_norm = normalize_username(acc.username)
            official_display_norm = normalize_display_name(acc.display_name)

            if candidate_username_norm and candidate_username_norm == official_username_norm:
                return {
                    "is_official": True,
                    "matched_asset_id": acc.asset_id,
                    "match_type": OfficialMatchTypeEnum.EXACT,
                    "confidence": 1.0,
                }

            if candidate_display_norm and candidate_display_norm == official_display_norm:
                return {
                    "is_official": True,
                    "matched_asset_id": acc.asset_id,
                    "match_type": OfficialMatchTypeEnum.EXACT,
                    "confidence": 1.0,
                }

            if candidate.profile_url and acc.profile_url:
                if candidate.profile_url.rstrip("/") == acc.profile_url.rstrip("/"):
                    return {
                        "is_official": True,
                        "matched_asset_id": acc.asset_id,
                        "match_type": OfficialMatchTypeEnum.EXACT,
                        "confidence": 1.0,
                    }

        return {
            "is_official": False,
            "matched_asset_id": None,
            "match_type": OfficialMatchTypeEnum.NONE,
            "confidence": 0.0,
        }

    def _create_official_result(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
        official_match: Dict[str, Any],
    ) -> SocialDetectionResult:
        threat_id = f"SOCIAL-THREAT-{uuid.uuid4().hex[:8].upper()}"

        detection_result = SocialDetectionResult(
            threat_id=threat_id,
            candidate_id=candidate.id,
            brand_id=candidate.brand_id,
            name_similarity=100.0,
            logo_similarity=100.0,
            branding_similarity=100.0,
            external_domain_similarity=100.0,
            lookalike_detected=False,
            lookalike_pattern=None,
            lookalike_similarity=None,
            lookalike_explanation=None,
            official_match_is_official=True,
            official_match_asset_id=official_match["matched_asset_id"],
            official_match_type=official_match["match_type"],
            official_match_confidence=official_match["confidence"],
            risk_score=0.0,
            risk_level=RiskLevelEnum.LOW,
            confidence=1.0,
            classification=ThreatClassificationEnum.OFFICIAL,
            reasons=["Account is registered as an official brand account"],
            source_type=candidate.collection_source,
            collected_at=candidate.collected_at,
            status=ThreatStatusEnum.NEW,
        )

        self.db.add(detection_result)
        self.db.flush()

        signal = SocialDetectionSignal(
            result_id=detection_result.id,
            name_similarity=100.0,
            logo_similarity=100.0,
            branding_similarity=100.0,
            external_domain_similarity=100.0,
            identifier_mismatch_score=0.0,
            official_mismatch=False,
            raw_signals={"official_match": official_match},
        )
        self.db.add(signal)
        self.db.commit()
        self.db.refresh(detection_result)

        return detection_result

    def _calculate_name_similarity(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> Optional[float]:
        names_to_compare = []

        if candidate.display_name:
            names_to_compare.append(candidate.display_name)
        if candidate.username:
            names_to_compare.append(candidate.username)

        if not names_to_compare:
            return None

        best_score = 0.0
        for name in names_to_compare:
            score = calculate_name_similarity(
                official_name=brand_profile.name,
                candidate_name=name,
                aliases=brand_profile.aliases,
                keywords=brand_profile.registered_names,
            )
            best_score = max(best_score, score)

        return round(best_score, 2)

    def _detect_lookalike(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> Dict[str, Any]:
        names_to_check = []
        if candidate.username:
            names_to_check.append(candidate.username)
        if candidate.display_name:
            names_to_check.append(candidate.display_name)

        best_detected = False
        best_pattern = None
        best_similarity = 0.0
        best_explanation = None

        for name in names_to_check:
            detected, pattern, similarity, explanation = detect_lookalike_pattern(
                official_name=brand_profile.name,
                candidate_name=name,
            )
            if detected and similarity > best_similarity:
                best_detected = True
                best_pattern = pattern
                best_similarity = similarity
                best_explanation = explanation

        return {
            "detected": best_detected,
            "pattern": best_pattern,
            "similarity": round(best_similarity, 2) if best_similarity > 0 else None,
            "explanation": best_explanation,
        }

    async def _calculate_logo_similarity(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> Optional[float]:
        if not candidate.profile_image_url and not candidate.logo_image_url:
            return None

        candidate_image = candidate.logo_image_url or candidate.profile_image_url
        official_logo = brand_profile.logo_url

        if not candidate_image or not official_logo:
            return None

        similarity, _ = compare_logo_with_official(candidate_image, official_logo)
        return round(similarity, 2) if similarity is not None else None

    def _calculate_branding_similarity(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> Optional[float]:
        signals = []
        weights = []

        if candidate.bio and brand_profile.brand_keywords:
            bio_lower = candidate.bio.lower()
            keyword_matches = sum(1 for kw in brand_profile.brand_keywords if kw.lower() in bio_lower)
            if brand_profile.brand_keywords:
                bio_score = (keyword_matches / len(brand_profile.brand_keywords)) * 100
                signals.append(bio_score)
                weights.append(0.4)

        if candidate.username:
            username_lower = candidate.username.lower()
            keyword_matches = sum(1 for kw in (brand_profile.brand_keywords or []) if kw.lower() in username_lower)
            if brand_profile.brand_keywords:
                username_score = (keyword_matches / len(brand_profile.brand_keywords)) * 100
                signals.append(username_score)
                weights.append(0.3)

        if candidate.display_name:
            name_sim = calculate_name_similarity(
                brand_profile.name,
                candidate.display_name,
                brand_profile.aliases,
                brand_profile.registered_names,
            )
            signals.append(name_sim)
            weights.append(0.3)

        if not signals:
            return None

        total_weight = sum(weights)
        weighted_sum = sum(s * w for s, w in zip(signals, weights))
        return round(weighted_sum / total_weight, 2)

    def _calculate_external_domain_similarity(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> Optional[float]:
        if not candidate.external_links:
            return None

        official_domain = brand_profile.official_domain
        if not official_domain:
            return None

        candidate_domains = []
        for url in candidate.external_links:
            domain = extract_domain_from_url(url)
            if domain:
                candidate_domains.append(domain)

        if not candidate_domains:
            return None

        from rapidfuzz import fuzz
        best_similarity = 0.0
        official_domain_lower = official_domain.lower()
        brand_name_lower = (brand_profile.name or "").lower().strip()
        suspicious_keywords = [
            "login",
            "secure",
            "verify",
            "support",
            "auth",
            "account",
            "confirm",
            "update",
            "signin",
            "password",
        ]

        for domain in candidate_domains:
            domain_lower = domain.lower()

            if brand_name_lower and brand_name_lower in domain_lower:
                if any(kw in domain_lower for kw in suspicious_keywords):
                    return 0.0

            similarity = fuzz.ratio(official_domain_lower, domain_lower)
            best_similarity = max(best_similarity, similarity)

        return round(best_similarity, 2)

    def _check_identifier_mismatch(
        self,
        candidate: SocialCandidate,
        brand_profile: BrandProfile,
    ) -> bool:
        if candidate.contact_information:
            email = candidate.contact_information.get("email")
            if email:
                email_domain = email.split("@")[-1].lower() if "@" in email else ""
                official_domain = (brand_profile.official_domain or "").lower()
                if official_domain and email_domain != official_domain:
                    return True

            phone = candidate.contact_information.get("phone")
            if phone and brand_profile.contact_phone:
                if phone != brand_profile.contact_phone:
                    return True

        return False