import hashlib
from typing import Optional, Tuple
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

try:
    from PIL import Image
    import imagehash
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL or imagehash not available, image similarity will be limited")


def download_image(url: str, timeout: int = 10) -> Optional[bytes]:
    try:
        import httpx
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                logger.warning(f"URL does not point to an image: {url}")
                return None
            return response.content
    except Exception as e:
        logger.warning(f"Failed to download image from {url}: {e}")
        return None


def compute_phash(image_data: bytes) -> Optional[str]:
    if not PIL_AVAILABLE:
        return None
    try:
        image = Image.open(BytesIO(image_data))
        if image.mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGB")
        phash = imagehash.phash(image)
        return str(phash)
    except Exception as e:
        logger.warning(f"Failed to compute perceptual hash: {e}")
        return None


def compute_dhash(image_data: bytes) -> Optional[str]:
    if not PIL_AVAILABLE:
        return None
    try:
        image = Image.open(BytesIO(image_data))
        if image.mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGB")
        dhash = imagehash.dhash(image)
        return str(dhash)
    except Exception as e:
        logger.warning(f"Failed to compute difference hash: {e}")
        return None


def compute_average_hash(image_data: bytes) -> Optional[str]:
    if not PIL_AVAILABLE:
        return None
    try:
        image = Image.open(BytesIO(image_data))
        if image.mode not in ("RGB", "RGBA", "L"):
            image = image.convert("RGB")
        ahash = imagehash.average_hash(image)
        return str(ahash)
    except Exception as e:
        logger.warning(f"Failed to compute average hash: {e}")
        return None


def hamming_distance(hash1: str, hash2: str) -> int:
    try:
        return bin(int(hash1, 16) ^ int(hash2, 16)).count("1")
    except Exception:
        return 64


def phash_similarity(hash1: Optional[str], hash2: Optional[str]) -> Optional[float]:
    if not hash1 or not hash2:
        return None
    distance = hamming_distance(hash1, hash2)
    max_distance = 64
    similarity = max(0.0, (1.0 - distance / max_distance) * 100)
    return similarity


def compare_images(
    image_url_1: Optional[str],
    image_url_2: Optional[str],
) -> Tuple[Optional[float], Optional[str]]:
    if not image_url_1 or not image_url_2:
        return None, "One or both image URLs are missing"

    if not PIL_AVAILABLE:
        return None, "Image processing libraries not available"

    image_data_1 = download_image(image_url_1)
    image_data_2 = download_image(image_url_2)

    if not image_data_1 or not image_data_2:
        return None, "Failed to download one or both images"

    phash1 = compute_phash(image_data_1)
    phash2 = compute_phash(image_data_2)

    if not phash1 or not phash2:
        return None, "Failed to compute perceptual hashes"

    similarity = phash_similarity(phash1, phash2)
    return similarity, f"Perceptual hash distance: {hamming_distance(phash1, phash2)}"


def compare_logo_with_official(
    candidate_logo_url: Optional[str],
    official_logo_url: Optional[str],
) -> Tuple[Optional[float], Optional[str]]:
    return compare_images(candidate_logo_url, official_logo_url)