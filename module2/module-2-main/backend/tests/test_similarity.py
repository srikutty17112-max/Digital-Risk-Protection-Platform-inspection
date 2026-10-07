from app.utils.similarity import (
    calculate_name_similarity,
    detect_lookalike_pattern,
    levenshtein_similarity,
    jaro_winkler_similarity,
)


class TestNameSimilarity:
    def test_exact_match(self):
        score = calculate_name_similarity("Brand Official", "Brand Official")
        assert score == 100.0

    def test_case_insensitive(self):
        score = calculate_name_similarity("Brand Official", "brand official")
        assert score == 100.0

    def test_similar_names(self):
        score = calculate_name_similarity("Brand Official", "Brand Offcial")
        assert score >= 85

    def test_missing_character(self):
        score = calculate_name_similarity("Brand Official", "Brand Offcial")
        assert score >= 85

    def test_added_word(self):
        score = calculate_name_similarity("Brand Official", "Brand Official Support")
        assert score >= 70

    def test_with_aliases(self):
        score = calculate_name_similarity("Brand Official", "Brand Off", aliases=["Brand Official"])
        assert score >= 85

    def test_no_match(self):
        score = calculate_name_similarity("Brand Official", "Completely Different")
        assert score < 50

    def test_empty_input(self):
        score = calculate_name_similarity("", "Brand Official")
        assert score == 0.0


class TestLookalikeDetection:
    def test_exact_match_not_lookalike(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "Brand Official")
        assert not detected
        assert pattern is None

    def test_character_swap(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "Brand Offciial")
        assert detected
        assert pattern == "CHARACTER_SWAP"

    def test_added_word(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "Brand Official Support")
        assert detected
        assert pattern == "ADDED_WORD"

    def test_removed_character(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "Brand")
        assert detected
        assert pattern == "REMOVED_CHARACTER"

    def test_case_variation(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "bRAND oFFICIAL")
        assert detected
        assert pattern == "CASE_VARIATION"

    def test_spacing_change(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("BrandOfficial", "Brand Official")
        assert detected or similarity >= 85

    def test_extra_character(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand", "Brandd")
        assert detected or similarity >= 65

    def test_no_lookalike_unrelated(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("Brand Official", "Unrelated Company")
        assert not detected or similarity < 70

    def test_empty_input(self):
        detected, pattern, similarity, explanation = detect_lookalike_pattern("", "Brand Official")
        assert not detected

    def test_similarity_range(self):
        for s in [levenshtein_similarity("a", "b"), jaro_winkler_similarity("a", "b")]:
            assert 0.0 <= s <= 100.0
