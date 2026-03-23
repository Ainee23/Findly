import difflib

def score_match(item_text: str, report_text: str) -> float:
    """
    Computes a text similarity score between 0.0 and 100.0.
    """
    if not item_text or not report_text:
        return 0.0
    matcher = difflib.SequenceMatcher(None, item_text.lower(), report_text.lower())
    return round(matcher.ratio() * 100, 2)

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
