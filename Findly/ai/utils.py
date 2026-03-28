import difflib
import imagehash
from PIL import Image

def text_similarity(text1: str, text2: str) -> float:
    """
    Computes purely built-in SequenceMatcher similarity score between 0.0 and 100.0.
    """
    if not text1 or not text2:
        return 0.0
    matcher = difflib.SequenceMatcher(None, text1.lower(), text2.lower())
    return round(matcher.ratio() * 100, 2)

def image_similarity(img1_path, img2_path) -> float:
    """
    Computes visual similarity using Perceptual Hashing (phash).
    Returns a score between 0.0 and 100.0.
    """
    if not img1_path or not img2_path:
        return 0.0
    try:
        hash1 = imagehash.phash(Image.open(img1_path))
        hash2 = imagehash.phash(Image.open(img2_path))
        diff = hash1 - hash2
        score = max(0.0, (1 - diff / 64.0)) * 100
        return round(score, 2)
    except Exception:
        return 0.0

def location_similarity(loc1: str, loc2: str, city1: str, city2: str) -> float:
    """
    Matches location and city. Same city is huge boost, same location is perfect.
    Returns 0.0 to 100.0
    """
    score = 0.0
    if city1 and city2 and city1.strip().lower() == city2.strip().lower():
        score += 50.0  # Same city is a great start
    
    if loc1 and loc2:
        matcher = difflib.SequenceMatcher(None, loc1.lower(), loc2.lower())
        loc_match = matcher.ratio() * 50.0
        score += loc_match

    return round(min(score, 100.0), 2)

def generate_item_description(title: str, category_name: str) -> str:
    """ Generates a boilerplate text description based on title and category. """
    title = title.strip() or "an item"
    cat = category_name.strip() if category_name else "various items"
    return f"Lost or found {title} belonging to the {cat} category. Please refer to the images or contact me for more specific details."

def suggest_category_for_title(title: str) -> str:
    """ Heuristically finds the best matching category name from existing categories. """
    try:
        from items.models import Category
        title_words = set(title.lower().split())
        categories = Category.objects.all()
        best_match = None
        best_score = 0
        for cat in categories:
            cat_words = set(cat.name.lower().split())
            overlap = len(title_words.intersection(cat_words))
            if overlap > best_score:
                best_score = overlap
                best_match = cat.name
        return best_match if best_match else ""
    except Exception:
        return ""
