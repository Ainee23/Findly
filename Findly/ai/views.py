from django.http import JsonResponse


def health(request):
    return JsonResponse({"ai": "ok", "note": "placeholder"})

