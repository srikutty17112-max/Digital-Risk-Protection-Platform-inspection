from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatClassification(str, Enum):
    OFFICIAL = "OFFICIAL"
    LIKELY_LEGITIMATE = "LIKELY_LEGITIMATE"
    SUSPICIOUS = "SUSPICIOUS"
    LIKELY_IMPERSONATION = "LIKELY_IMPERSONATION"
    HIGH_RISK_IMPERSONATION = "HIGH_RISK_IMPERSONATION"


@dataclass
class RiskWeights:
    NAME_SIMILARITY: float = 25.0
    LOGO_SIMILARITY: float = 25.0
    BRANDING_SIMILARITY: float = 15.0
    OFFICIAL_MISMATCH: float = 15.0
    EXTERNAL_DOMAIN: float = 10.0
    IDENTIFIER_MISMATCH: float = 10.0

    def total(self) -> float:
        return (
            self.NAME_SIMILARITY
            + self.LOGO_SIMILARITY
            + self.BRANDING_SIMILARITY
            + self.OFFICIAL_MISMATCH
            + self.EXTERNAL_DOMAIN
            + self.IDENTIFIER_MISMATCH
        )


DEFAULT_WEIGHTS = RiskWeights()


def calculate_risk_score(
    name_similarity: Optional[float],
    logo_similarity: Optional[float],
    branding_similarity: Optional[float],
    external_domain_similarity: Optional[float],
    official_mismatch: bool,
    identifier_mismatch: bool,
    weights: Optional[RiskWeights] = None,
) -> float:
    if weights is None:
        weights = DEFAULT_WEIGHTS

    available_weight = 0.0
    weighted_sum = 0.0

    if name_similarity is not None:
        available_weight += weights.NAME_SIMILARITY
        weighted_sum += (name_similarity / 100.0) * weights.NAME_SIMILARITY

    if logo_similarity is not None:
        available_weight += weights.LOGO_SIMILARITY
        weighted_sum += (logo_similarity / 100.0) * weights.LOGO_SIMILARITY

    if branding_similarity is not None:
        available_weight += weights.BRANDING_SIMILARITY
        weighted_sum += (branding_similarity / 100.0) * weights.BRANDING_SIMILARITY

    if external_domain_similarity:
        available_weight += weights.EXTERNAL_DOMAIN
        domain_risk = 100.0 - external_domain_similarity
        weighted_sum += (domain_risk / 100.0) * weights.EXTERNAL_DOMAIN

    if official_mismatch:
        available_weight += weights.OFFICIAL_MISMATCH
        weighted_sum += 1.0 * weights.OFFICIAL_MISMATCH

    if identifier_mismatch:
        available_weight += weights.IDENTIFIER_MISMATCH
        weighted_sum += 1.0 * weights.IDENTIFIER_MISMATCH

    if available_weight == 0:
        return 0.0

    normalized_score = (weighted_sum / available_weight) * 100
    return round(min(100.0, max(0.0, normalized_score)), 2)


def determine_risk_level(risk_score: float) -> RiskLevel:
    if risk_score >= 80:
        return RiskLevel.CRITICAL
    elif risk_score >= 60:
        return RiskLevel.HIGH
    elif risk_score >= 30:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.LOW


def determine_classification(
    risk_score: float,
    risk_level: RiskLevel,
    is_official: bool,
    name_similarity: Optional[float],
    logo_similarity: Optional[float],
    branding_similarity: Optional[float],
    lookalike_detected: bool,
    external_domain_suspicious: bool,
    confidence: float,
) -> ThreatClassification:
    if is_official:
        return ThreatClassification.OFFICIAL

    if risk_level == RiskLevel.LOW:
        if name_similarity and name_similarity >= 70:
            return ThreatClassification.SUSPICIOUS
        return ThreatClassification.LIKELY_LEGITIMATE

    if risk_level == RiskLevel.MEDIUM:
        if lookalike_detected and name_similarity and name_similarity >= 80:
            return ThreatClassification.LIKELY_IMPERSONATION
        return ThreatClassification.SUSPICIOUS

    if risk_level == RiskLevel.HIGH:
        if (logo_similarity and logo_similarity >= 70) or (
            branding_similarity and branding_similarity >= 70
        ):
            return ThreatClassification.HIGH_RISK_IMPERSONATION
        return ThreatClassification.LIKELY_IMPERSONATION

    if risk_level == RiskLevel.CRITICAL:
        return ThreatClassification.HIGH_RISK_IMPERSONATION

    return ThreatClassification.LIKELY_LEGITIMATE


def calculate_confidence(
    name_similarity: Optional[float],
    logo_similarity: Optional[float],
    branding_similarity: Optional[float],
    external_domain_similarity: Optional[float],
    has_profile_image: bool,
    has_bio: bool,
    has_external_links: bool,
    official_match_confidence: float,
) -> float:
    evidence_count = 0
    evidence_quality = 0.0

    if name_similarity is not None:
        evidence_count += 1
        evidence_quality += min(name_similarity / 100.0, 1.0)

    if logo_similarity is not None:
        evidence_count += 1
        evidence_quality += min(logo_similarity / 100.0, 1.0)

    if branding_similarity is not None:
        evidence_count += 1
        evidence_quality += min(branding_similarity / 100.0, 1.0)

    if external_domain_similarity is not None:
        evidence_count += 1
        evidence_quality += (1.0 - external_domain_similarity / 100.0)

    if has_profile_image:
        evidence_count += 1
        evidence_quality += 0.5

    if has_bio:
        evidence_count += 1
        evidence_quality += 0.3

    if has_external_links:
        evidence_count += 1
        evidence_quality += 0.3

    evidence_count += 1
    evidence_quality += official_match_confidence

    if evidence_count == 0:
        return 0.0

    base_confidence = evidence_quality / evidence_count
    confidence = min(1.0, base_confidence * 1.2)
    return round(confidence, 2)


def generate_reasons(
    name_similarity: Optional[float],
    logo_similarity: Optional[float],
    branding_similarity: Optional[float],
    external_domain_similarity: Optional[float],
    official_match: Dict[str, Any],
    lookalike: Dict[str, Any],
    identifier_mismatch: bool,
    candidate_data: Dict[str, Any],
) -> List[str]:
    reasons = []

    if official_match.get("is_official"):
        reasons.append("Account is registered as an official brand account")
        return reasons

    if not official_match.get("is_official"):
        reasons.append("Account is not registered as an official brand account")

    if name_similarity is not None:
        if name_similarity >= 90:
            reasons.append("Display name is highly similar to the official brand name")
        elif name_similarity >= 70:
            reasons.append("Display name is moderately similar to the official brand name")
        elif name_similarity >= 50:
            reasons.append("Display name has some similarity to the official brand name")

    if lookalike.get("detected"):
        pattern = lookalike.get("pattern")
        explanations = {
            "CHARACTER_SWAP": "Username contains a character swap variation of the brand name",
            "ADDED_WORD": "Username contains the brand name with an additional word",
            "REMOVED_CHARACTER": "Username is missing characters from the brand name",
            "EXTRA_CHARACTER": "Username has extra characters compared to the brand name",
            "SPACING_CHANGE": "Username uses different spacing in the brand name",
            "PUNCTUATION_CHANGE": "Username uses different punctuation in the brand name",
            "CHARACTER_SUBSTITUTION": "Username has character substitutions (e.g., numbers for letters)",
            "CASE_VARIATION": "Username uses unusual casing for the brand name",
        }
        if pattern in explanations:
            reasons.append(explanations[pattern])

    if logo_similarity is not None:
        if logo_similarity >= 80:
            reasons.append("Profile image is highly similar to the official brand logo")
        elif logo_similarity >= 50:
            reasons.append("Profile image has moderate similarity to the official brand logo")

    if branding_similarity is not None:
        if branding_similarity >= 70:
            reasons.append("Account bio and branding closely mimic the official brand")
        elif branding_similarity >= 40:
            reasons.append("Account bio contains brand-related keywords and terminology")

    if external_domain_similarity is not None:
        if external_domain_similarity < 30:
            reasons.append("External domain differs significantly from the official brand domain")
        elif external_domain_similarity < 60:
            reasons.append("External domain has low similarity to the official brand domain")

    if identifier_mismatch:
        reasons.append("Contact information does not match official brand identifiers")

    if candidate_data.get("verification_status"):
        if candidate_data["verification_status"].lower() in ["verified", "blue_verified"]:
            reasons.append("Account has platform verification (may be misleading)")

    if not reasons:
        reasons.append("Insufficient evidence for classification")

    return reasons


def assess_false_positive_risk(
    name_similarity: Optional[float],
    logo_similarity: Optional[float],
    branding_similarity: Optional[float],
    lookalike_detected: bool,
    official_keywords: List[str],
    candidate_bio: Optional[str],
) -> Tuple[bool, Optional[str]]:
    if name_similarity and name_similarity >= 80:
        if logo_similarity is None and branding_similarity is None:
            if not lookalike_detected:
                common_words = ["support", "help", "careers", "jobs", "official", "news", "updates"]
                candidate_lower = (candidate_bio or "").lower()
                if any(word in candidate_lower for word in common_words):
                    return True, "Name similarity detected, but insufficient impersonation evidence (no logo/branding match)"

    if name_similarity and name_similarity >= 70:
        generic_terms = ["tech", "technology", "solutions", "services", "group", "inc", "llc", "ltd"]
        official_lower = " ".join(official_keywords).lower()
        candidate_lower = (candidate_bio or "").lower()
        if any(term in official_lower for term in generic_terms):
            if not lookalike_detected and logo_similarity is None:
                return True, "Generic company name match - requires additional signals"

    return False, None
