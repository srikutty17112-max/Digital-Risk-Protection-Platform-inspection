from typing import Optional, List, Tuple
from rapidfuzz import fuzz, process
import re


def levenshtein_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    return fuzz.ratio(s1, s2)


def jaro_winkler_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    return fuzz.WRatio(s1, s2)


def token_set_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    return fuzz.token_set_ratio(s1, s2)


def token_sort_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    return fuzz.token_sort_ratio(s1, s2)


def partial_ratio_similarity(s1: str, s2: str) -> float:
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    return fuzz.partial_ratio(s1, s2)


def calculate_name_similarity(
    official_name: str,
    candidate_name: str,
    aliases: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
) -> float:
    if not official_name or not candidate_name:
        return 0.0

    official_norm = official_name.lower().strip()
    candidate_norm = candidate_name.lower().strip()

    if official_norm == candidate_norm:
        return 100.0

    scores = [
        levenshtein_similarity(official_norm, candidate_norm),
        jaro_winkler_similarity(official_norm, candidate_norm),
        token_set_similarity(official_norm, candidate_norm),
        token_sort_similarity(official_norm, candidate_norm),
    ]

    if aliases:
        for alias in aliases:
            alias_norm = alias.lower().strip()
            if alias_norm:
                scores.append(levenshtein_similarity(alias_norm, candidate_norm))
                scores.append(token_set_similarity(alias_norm, candidate_norm))

    if keywords:
        for kw in keywords:
            kw_norm = kw.lower().strip()
            if kw_norm and kw_norm in candidate_norm:
                scores.append(90.0)

    return max(scores) if scores else 0.0


def detect_lookalike_pattern(
    official_name: str,
    candidate_name: str,
) -> Tuple[bool, Optional[str], float, Optional[str]]:
    if not official_name or not candidate_name:
        return False, None, 0.0, None

    official_norm = official_name.lower().strip()
    candidate_norm = candidate_name.lower().strip()

    official_clean = re.sub(r"[^\w\s]", "", official_norm)
    candidate_clean = re.sub(r"[^\w\s]", "", candidate_norm)

    official_tokens = official_clean.split()
    candidate_tokens = candidate_clean.split()

    if not official_tokens or not candidate_tokens:
        return False, None, 0.0, None

    similarity = levenshtein_similarity(official_clean, candidate_clean)

    official_no_space = official_clean.replace(" ", "")
    candidate_no_space = candidate_clean.replace(" ", "")

    if len(candidate_tokens) == len(official_tokens) + 1:
        for token in candidate_tokens:
            if token not in official_tokens:
                if len(token) > 2:
                    return (
                        True,
                        "ADDED_WORD",
                        similarity,
                        f"Candidate contains the protected brand name with an additional word: '{token}'",
                    )

    if len(official_tokens) == len(candidate_tokens) + 1:
        for token in official_tokens:
            if token not in candidate_tokens:
                return (
                    True,
                    "REMOVED_CHARACTER",
                    similarity,
                    f"Candidate is missing a word from the official brand name: '{token}'",
                )

    if similarity >= 95:
        if official_no_space == candidate_no_space:
            if official_clean.lower() != candidate_clean.lower():
                return (
                    True,
                    "SPACING_CHANGE",
                    similarity,
                    "Candidate uses different spacing in the brand name",
                )

    if similarity >= 85:
        if official_no_space != candidate_no_space:
            if official_no_space == candidate_no_space:
                if official_clean.lower() != candidate_clean.lower():
                    return (
                        True,
                        "SPACING_CHANGE",
                        similarity,
                        "Candidate uses different spacing in the brand name",
                    )

    if similarity >= 80:
        official_no_punct = re.sub(r"[^\w]", "", official_norm)
        candidate_no_punct = re.sub(r"[^\w]", "", candidate_norm)
        if official_no_punct != candidate_no_punct:
            if official_no_punct == candidate_no_punct:
                return (
                    True,
                    "PUNCTUATION_CHANGE",
                    similarity,
                    "Candidate uses different punctuation in the brand name",
                )

    if similarity >= 75:
        official_for_case = official_name.lower().strip()
        candidate_for_case = candidate_name.lower().strip()
        if official_for_case == candidate_for_case and official_name.strip() != candidate_name.strip():
            return (
                True,
                "CASE_VARIATION",
                similarity,
                "Candidate uses different casing for the brand name",
            )

    if similarity >= 70:
        official_chars = list(official_clean.replace(" ", ""))
        candidate_chars = list(candidate_clean.replace(" ", ""))
        if len(official_chars) == len(candidate_chars):
            diff_count = sum(1 for a, b in zip(official_chars, candidate_chars) if a != b)
            if diff_count == 1:
                return (
                    True,
                    "CHARACTER_SUBSTITUTION",
                    similarity,
                    "Candidate has a single character substitution",
                )
            if diff_count == 2:
                for i in range(len(official_chars) - 1):
                    if (
                        official_chars[i] == candidate_chars[i + 1]
                        and official_chars[i + 1] == candidate_chars[i]
                    ):
                        return (
                            True,
                            "CHARACTER_SWAP",
                            similarity,
                            "Candidate has adjacent characters swapped",
                        )

    if similarity >= 65:
        if len(candidate_clean) > len(official_clean):
            extra = len(candidate_clean) - len(official_clean)
            if extra <= 2:
                return (
                    True,
                    "EXTRA_CHARACTER",
                    similarity,
                    f"Candidate has {extra} extra character(s)",
                )

    return False, None, similarity, None


def calculate_best_similarity(
    official_name: str,
    candidate_name: str,
    official_aliases: Optional[List[str]] = None,
    official_keywords: Optional[List[str]] = None,
) -> Tuple[float, Optional[str], Optional[str]]:
    similarity = calculate_name_similarity(
        official_name, candidate_name, official_aliases, official_keywords
    )

    detected, pattern, lookalike_sim, explanation = detect_lookalike_pattern(
        official_name, candidate_name
    )

    return similarity, pattern if detected else None, explanation