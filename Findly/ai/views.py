import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from items.models import Item, Category
from .utils import text_similarity, image_similarity, location_similarity, generate_item_description, suggest_category_for_title

def health(request):
    return JsonResponse({"ai": "ok", "note": "heuristic matching active"})

@require_http_methods(["GET"])
def ai_match(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
        
    target_status = Item.Status.FOUND if item.status == Item.Status.LOST else Item.Status.LOST
    candidates = Item.objects.filter(status=target_status).exclude(id=item.id)
    
    matches = []
    item_text = f"{item.title} {item.description} {item.category.name if item.category else ''}"
    
    for candidate in candidates:
        candidate_text = f"{candidate.title} {candidate.description} {candidate.category.name if candidate.category else ''}"
        
        # 50% Text Score
        t_score = text_similarity(item_text, candidate_text) * 0.50
        
        # 30% Image Score
        # Try comparing primary images if both exist
        i_score = 0.0
        try:
            if item.image and candidate.image:
                i_score = image_similarity(item.image.path, candidate.image.path) * 0.30
        except Exception:
            pass
            
        # 20% Location Score
        l_score = location_similarity(item.location, candidate.location, item.city, candidate.city) * 0.20
        
        final_score = t_score + i_score + l_score
        
        if final_score > 25: # Keep the threshold realistic
            matches.append({
                "id": candidate.id,
                "title": candidate.title,
                "score": round(final_score, 2),
                "url": f"/items/{candidate.id}/" # Base generic url, the frontend constructs this further if needed
            })
            
    matches.sort(key=lambda x: x["score"], reverse=True)
    return JsonResponse({"matches": matches[:5]})

@require_http_methods(["GET"])
def ai_search(request):
    query = request.GET.get('q', '').lower()
    if len(query) < 2:
        return JsonResponse({"suggestions": []})
        
    items = Item.objects.filter(title__icontains=query)[:20]
    suggestions = [item.title for item in items]
    return JsonResponse({"suggestions": list(set(suggestions))[:7]})

@require_http_methods(["GET", "POST"])
def ai_suggest(request):
    title = request.GET.get('title', '')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', '')
        except json.JSONDecodeError:
            pass
            
    if not title:
        return JsonResponse({"category": ""})
        
    suggested = suggest_category_for_title(title)
    return JsonResponse({"category": suggested})

@require_http_methods(["GET", "POST"])
def ai_generate_description(request):
    title = request.GET.get('title', '')
    category = request.GET.get('category', '')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', title)
            category = data.get('category', category)
        except json.JSONDecodeError:
            pass
            
    description = generate_item_description(title, category)
    return JsonResponse({"description": description})
