import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from items.models import Item
from notifications.utils import notify

from .forms import MessageForm
from .models import Message, Thread

User = get_user_model()  # ✅ Use custom email-based User


@login_required
def inbox(request):
    threads = (
        Thread.objects.filter(participants=request.user)
        .annotate(last_msg_at=Max("messages__created_at"))
        .order_by("-last_msg_at", "-updated_at")
    )
    return render(request, "messaging/inbox.html", {"threads": threads})


@login_required
def thread_detail(request, pk: int):
    thread = get_object_or_404(Thread, pk=pk, participants=request.user)
    msgs = thread.messages.select_related("sender").order_by("created_at")
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg: Message = form.save(commit=False)
            msg.thread = thread
            msg.sender = request.user
            msg.save()
            thread.save(update_fields=["updated_at"])
            for u in thread.participants.exclude(pk=request.user.pk):
                notify(
                    u,
                    f"New message from {request.user.email}",  # ✅ email not username
                    link=f"/messaging/thread/{thread.pk}/"
                )
            return redirect("messaging:thread", pk=thread.pk)
    else:
        form = MessageForm()
    return render(
        request,
        "messaging/thread.html",
        {"thread": thread, "messages": msgs, "form": form}
    )


@login_required
def start_thread(request, item_pk: int):
    item = get_object_or_404(Item.objects.select_related("owner"), pk=item_pk)
    if item.owner_id == request.user.id:
        messages.error(request, "You can't message yourself.")
        return redirect("items:detail", pk=item.pk)

    existing = (
        Thread.objects.filter(item=item, participants=request.user)
        .filter(participants=item.owner)
        .distinct()
        .first()
    )
    if existing:
        return redirect("messaging:thread", pk=existing.pk)

    thread = Thread.objects.create(item=item)
    thread.participants.add(request.user, item.owner)
    notify(
        item.owner,
        f"{request.user.email} started a chat about '{item.title}'",  # ✅ email not username
        link=f"/messaging/thread/{thread.pk}/"
    )
    return redirect("messaging:thread", pk=thread.pk)


@login_required
@require_POST
def edit_message(request, message_id: int):
    msg = get_object_or_404(Message, pk=message_id)
    if msg.sender != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        data = json.loads(request.body)
        new_body = data.get("body", "").strip()
        if not new_body:
            return JsonResponse({"error": "Message body cannot be empty"}, status=400)
        
        msg.body = new_body
        msg.is_edited = True
        msg.save(update_fields=["body", "is_edited"])
        return JsonResponse({"success": True, "new_body": msg.body})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@login_required
@require_POST
def delete_message(request, message_id: int):
    msg = get_object_or_404(Message, pk=message_id)
    if msg.sender != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    msg.delete()
    return JsonResponse({"success": True})
