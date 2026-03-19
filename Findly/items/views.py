from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.db.models import Count

from .models import ClaimRequest, Item, Category, ItemVerification
from .forms import ItemForm, ItemVerificationForm, ClaimRequestForm
from notifications.models import Notification


@login_required
def verify_item(request, pk):

    item = get_object_or_404(Item, pk=pk)

    if request.method == "POST":

        form = ItemVerificationForm(request.POST, request.FILES)

        if form.is_valid():

            verification = form.save(commit=False)

            verification.item = item
            verification.owner = request.user

            verification.save()

            return redirect("items:detail", pk=item.pk)

    else:
        form = ItemVerificationForm()

    return render(
        request,
        "items/verify_item.html",
        {
            "form": form,
            "item": item,
        },
    )


def item_list(request):

    items = Item.objects.exclude(status="closed")

    q = request.GET.get("q")
    status = request.GET.get("status")
    city = request.GET.get("city")
    category = request.GET.get("category")


    if q:
        items = items.filter(title__icontains=q)


    if status:
        items = items.filter(status=status)


    if city:
        items = items.filter(city__icontains=city)


    if category:
        items = items.filter(category_id=category)


    categories = Category.objects.all()


    return render(
        request,
        "items/list.html",
        {
            "items": items,
            "categories": categories,
        },
    )
    
def item_detail(request, pk):

    item = Item.objects.get(pk=pk)

    # get latest verification for this item
    verification = ItemVerification.objects.filter(
        item=item
    ).last()

    claims = item.claims.order_by("-created_at")
    user_claim = None
    if request.user.is_authenticated:
        user_claim = claims.filter(sender=request.user).first()

    return render(
        request,
        "items/detail.html",
        {
            "item": item,
            "verification": verification,
            "claims": claims,
            "user_claim": user_claim,
        }
    )


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, "Item posted.")
            return redirect("items:detail", pk=item.pk)
    else:
        form = ItemForm()
    return render(request, "items/create.html", {"form": form})


@login_required
def my_items(request):
    qs = Item.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "items/my_items.html", {"items": qs})

@login_required
def update_location(request, pk):
    """Update an item's stored lat/lng via AJAX.

    Only the item owner may update the location.
    """

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

    try:
        item = Item.objects.get(id=pk)
    except Item.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Item not found"}, status=404)

    if item.owner != request.user:
        return JsonResponse({"status": "error", "message": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body)
        lat = data.get("lat")
        lng = data.get("lng")
    except Exception:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    if lat is None or lng is None:
        return JsonResponse({"status": "error", "message": "Missing coordinates"}, status=400)

    item.latitude = lat
    item.longitude = lng
    item.location_updated_at = timezone.now()
    item.save()

    return JsonResponse({"status": "ok", "lat": lat, "lng": lng})


@login_required
def change_status(request, pk, status):

    item = Item.objects.get(id=pk)

    if item.owner != request.user:
        return redirect("items:detail", pk=pk)

    item.status = status
    item.save()

    return redirect("items:detail", pk=pk)

def _get_map_items_queryset(request):
    """Build the queryset for map items based on request filters."""

    items = Item.objects.exclude(
        latitude__isnull=True,
        longitude__isnull=True
    ).exclude(status="closed")

    status = request.GET.get("status")
    category = request.GET.get("category")
    q = request.GET.get("q")

    if status:
        items = items.filter(status=status)

    if category:
        items = items.filter(category_id=category)

    if q:
        items = items.filter(title__icontains=q)

    return items


def map_items_json(request):
    """Endpoint for returning map marker data as JSON."""

    items = _get_map_items_queryset(request)

    data = [
        {
            "id": item.id,
            "title": item.title,
            "status": item.status,
            "category": item.category.name if item.category else None,
            "lat": item.latitude,
            "lng": item.longitude,
            "url": request.build_absolute_uri(reverse('items:detail', args=[item.pk])),
        }
        for item in items
    ]

    return JsonResponse({"items": data})


def map_view(request):
    items = _get_map_items_queryset(request)

    # ensure we only render items that have coordinates
    items = items.exclude(latitude__isnull=True, longitude__isnull=True)

    categories = Category.objects.all()

    return render(
        request,
        "items/map.html",
        {
            "items": items,
            "status_choices": Item.Status.choices,
            "categories": categories,
            "filter_status": request.GET.get("status", ""),
            "filter_category": request.GET.get("category", ""),
            "focus_item": request.GET.get("focus", ""),
            "query": request.GET.get("q", ""),
        },
    )
    
@login_required
def dashboard(request):

    total = Item.objects.count()

    lost = Item.objects.filter(status="lost").count()

    found = Item.objects.filter(status="found").count()

    mine = Item.objects.filter(owner=request.user).count()


    return render(
        request,
        "items/dashboard.html",
        {
            "total": total,
            "lost": lost,
            "found": found,
            "mine": mine,
        }
    )
    
def confirm_owner(request, pk):

    verification = get_object_or_404(
        ItemVerification,
        pk=pk
    )

    if request.user != verification.item.owner:
        return redirect("dashboard:home")

    verification.finder_confirmed = True
    verification.save()

    return redirect("items:detail", pk=verification.item.pk)

@login_required
def send_claim(request, pk):
    """Allow a user to file a claim for an item and optionally attach proof."""

    item = get_object_or_404(Item, pk=pk)

    if request.user == item.owner:
        return redirect("items:detail", pk=pk)

    # Allow claims on both lost and found items
    if item.status not in ["lost", "found"]:
        return redirect("items:detail", pk=pk)

    existing = ClaimRequest.objects.filter(
        item=item,
        sender=request.user,
        approved=False,
        rejected=False,
    ).first()

    if existing:
        return redirect("items:detail", pk=pk)

    if request.method == "POST":
        form = ClaimRequestForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.sender = request.user
            claim.save()

            Notification.objects.create(
                user=item.owner,
                verb=f"New claim for '{item.title}'",
                link=reverse('items:detail', args=[item.pk]),
            )

            messages.success(request, "Your claim request has been submitted.")
            return redirect("items:detail", pk=pk)
    else:
        form = ClaimRequestForm()

    return render(request, "items/claim_request.html", {"item": item, "form": form})


@login_required
def edit_claim(request, pk):
    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.sender:
        return redirect("dashboard:home")

    if claim.approved or claim.rejected:
        return redirect("items:detail", pk=claim.item.pk)

    if request.method == "POST":
        form = ClaimRequestForm(request.POST, request.FILES, instance=claim)
        if form.is_valid():
            form.save()
            messages.success(request, "Your claim has been updated.")
            return redirect("items:detail", pk=claim.item.pk)
    else:
        form = ClaimRequestForm(instance=claim)

    return render(request, "items/claim_request.html", {"item": claim.item, "form": form, "claim": claim})


@login_required
def accept_claim(request, pk):

    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.item.owner:
        return redirect("dashboard:home")

    claim.approved = True
    claim.rejected = False
    claim.proof_requested = False
    claim.save()

    # Keep the item active until pickup is confirmed (so parties can coordinate).
    # It will be closed when pickup is confirmed.

    Notification.objects.create(
        user=claim.sender,
        verb=f"Your claim for '{claim.item.title}' was approved",
        link=reverse('items:detail', args=[claim.item.pk]),
    )

    messages.success(request, "Claim approved. Please coordinate with the finder to share live locations and arrange pickup.")

    return redirect("items:detail", pk=claim.item.pk)


@login_required
def reject_claim(request, pk):

    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.item.owner:
        return redirect("dashboard:home")

    claim.rejected = True
    claim.approved = False
    claim.proof_requested = False
    claim.save()

    Notification.objects.create(
        user=claim.sender,
        verb=f"Your claim for '{claim.item.title}' was rejected",
        link=reverse('items:detail', args=[claim.item.pk]),
    )

    messages.success(request, "Claim rejected.")

    return redirect("items:detail", pk=claim.item.pk)


@login_required
def request_claim_proof(request, pk):

    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.item.owner:
        return redirect("dashboard:home")

    if request.method == "POST":
        note = request.POST.get("owner_response", "").strip()
        claim.proof_requested = True
        claim.owner_response = note
        claim.save()
        Notification.objects.create(
            user=claim.sender,
            verb=f"Owner requested more proof for '{claim.item.title}'",
            link=reverse('items:detail', args=[claim.item.pk]),
        )
        messages.success(request, "Proof requested from the finder.")

    return redirect("items:detail", pk=claim.item.pk)


@login_required
def update_claim_location(request, pk):
    """Allow the finder to share live location after claim approval."""

    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.sender:
        return JsonResponse({"status": "error", "message": "Permission denied."}, status=403)

    if not claim.approved or claim.pickup_confirmed:
        return JsonResponse({"status": "error", "message": "Cannot update location at this time."}, status=400)

    try:
        data = json.loads(request.body)
        lat = data.get("lat")
        lng = data.get("lng")
    except Exception:
        return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)

    if lat is None or lng is None:
        return JsonResponse({"status": "error", "message": "Missing coordinates."}, status=400)

    claim.finder_lat = lat
    claim.finder_lng = lng
    claim.finder_location_updated_at = timezone.now()
    claim.save()

    return JsonResponse({"status": "ok"})


@login_required
def confirm_pickup(request, pk):
    """Finder confirms pickup; closes the item and allows review."""

    claim = get_object_or_404(ClaimRequest, pk=pk)

    if request.user != claim.sender:
        return redirect("dashboard:home")

    if not claim.approved or claim.rejected:
        return redirect("items:detail", pk=claim.item.pk)

    if request.method == "POST":
        claim.pickup_confirmed = True
        claim.pickup_confirmed_at = timezone.now()
        claim.save()

        claim.item.status = "closed"
        claim.item.save()

        # Some custom user models may not implement get_full_name()
        user_display = None
        if hasattr(request.user, 'get_full_name') and callable(getattr(request.user, 'get_full_name')):
            user_display = request.user.get_full_name() or None
        if not user_display:
            user_display = getattr(request.user, 'email', str(request.user))

        Notification.objects.create(
            user=claim.item.owner,
            verb=f"{user_display} confirmed pickup of '{claim.item.title}'",
            link=reverse('items:detail', args=[claim.item.pk]),
        )

        messages.success(request, "Pickup confirmed. Item is now closed.")

    return redirect("items:detail", pk=claim.item.pk)
