from app.utils.risk_scoring import (
    calculate_risk_score,
    determine_risk_level,
    determine_classification,
    calculate_confidence,
    generate_reasons,
    assess_false_positive_risk,
    DEFAULT_WEIGHTS,
)


class TestRiskScore:
    def test_zero_risk(self):
        score = calculate_risk_score(
            name_similarity=0.0,
            logo_similarity=0.0,
            branding_similarity=0.0,
            external_domain_similarity=0.0,
            official_mismatch=False,
            identifier_mismatch=False,
        )
        assert score == 0.0

    def test_max_risk(self):
        score = calculate_risk_score(
            name_similarity=100.0,
            logo_similarity=100.0,
            branding_similarity=100.0,
            external_domain_similarity=0.0,
            official_mismatch=True,
            identifier_mismatch=True,
        )
        assert score == 100.0

    def test_within_valid_range(self):
        score = calculate_risk_score(
            name_similarity=50.0,
            logo_similarity=70.0,
            branding_similarity=30.0,
            external_domain_similarity=20.0,
            official_mismatch=True,
            identifier_mismatch=False,
        )
        assert 0.0 <= score <= 100.0

    def test_no_weights_returns_zero(self):
        score = calculate_risk_score(
            name_similarity=None,
            logo_similarity=None,
            branding_similarity=None,
            external_domain_similarity=None,
            official_mismatch=False,
            identifier_mismatch=False,
        )
        assert score == 0.0


class TestRiskLevel:
    def test_low(self):
        level = determine_risk_level(20.0)
        assert level.value == "LOW"

    def test_medium(self):
        level = determine_risk_level(50.0)
        assert level.value == "MEDIUM"

    def test_high(self):
        level = determine_risk_level(70.0)
        assert level.value == "HIGH"

    def test_critical(self):
        level = determine_risk_level(90.0)
        assert level.value == "CRITICAL"


class TestConfidence:
    def test_within_valid_range(self):
        confidence = calculate_confidence(
            name_similarity=80.0,
            logo_similarity=90.0,
            branding_similarity=70.0,
            external_domain_similarity=20.0,
            has_profile_image=True,
            has_bio=True,
            has_external_links=True,
            official_match_confidence=1.0,
        )
        assert 0.0 <= confidence <= 1.0

    def test_no_evidence(self):
        confidence = calculate_confidence(
            name_similarity=None,
            logo_similarity=None,
            branding_similarity=None,
            external_domain_similarity=None,
            has_profile_image=False,
            has_bio=False,
            has_external_links=False,
            official_match_confidence=0.0,
        )
        assert confidence == 0.0


class TestReasons:
    def test_non_empty_for_suspicious(self):
        reasons = generate_reasons(
            name_similarity=90.0,
            logo_similarity=80.0,
            branding_similarity=70.0,
            external_domain_similarity=20.0,
            official_match={"is_official": False},
            lookalike={"detected": True, "pattern": "CHARACTER_SWAP"},
            identifier_mismatch=True,
            candidate_data={"verification_status": "verified", "bio": "test", "external_links": ["http://example.com"]},
        )
        assert len(reasons) > 0
        assert all(isinstance(r, str) and r for r in reasons)

    def test_official_reason(self):
        reasons = generate_reasons(
            name_similarity=100.0,
            logo_similarity=100.0,
            branding_similarity=100.0,
            external_domain_similarity=100.0,
            official_match={"is_official": True},
            lookalike={"detected": False},
            identifier_mismatch=False,
            candidate_data={},
        )
        assert len(reasons) > 0
        assert any("official" in r.lower() for r in reasons)

    def test_insufficient_evidence_fallback(self):
        reasons = generate_reasons(
            name_similarity=None,
            logo_similarity=None,
            branding_similarity=None,
            external_domain_similarity=None,
            official_match={"is_official": False},
            lookalike={"detected": False},
            identifier_mismatch=False,
            candidate_data={},
        )
        assert len(reasons) > 0


class TestFalsePositiveRisk:
    def test_name_similarity_no_evidence(self):
        is_fp, reason = assess_false_positive_risk(
            name_similarity=85.0,
            logo_similarity=None,
            branding_similarity=None,
            lookalike_detected=False,
            official_keywords=["venture capital"],
            candidate_bio="Support account for Brand Official",
        )
        assert is_fp is True

    def test_no_false_positive_with_evidence(self):
        is_fp, reason = assess_false_positive_risk(
            name_similarity=85.0,
            logo_similarity=90.0,
            branding_similarity=80.0,
            lookalike_detected=True,
            official_keywords=["venture capital"],
            candidate_bio="Support account for Brand Official",
        )
        assert is_fp is False
