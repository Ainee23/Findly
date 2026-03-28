import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from items.models import Item
from notifications.utils import notify
from dashboard.models import ActivityLog

from .forms import MessageForm
from .models import Message, Thread

User = get_user_model()  # ✅ Use custom email-based User


def get_user_threads(user):
    from django.db.models import Prefetch, Q, Count
    return (
        Thread.objects.filter(participants=user)
        .annotate(last_msg_at=Max("messages__created_at"))
        .annotate(unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=user)))
        .prefetch_related(Prefetch("participants", queryset=User.objects.select_related("profile")))
        .order_by("-last_msg_at", "-updated_at")
    )


@login_required
def inbox(request):
    threads = get_user_threads(request.user)
    return render(request, "messaging/inbox.html", {"threads": threads, "active_thread": None})


@login_required
def thread_detail(request, pk: int):
    thread = get_object_or_404(Thread, pk=pk, participants=request.user)
    
    # Mark messages as read
    thread.messages.exclude(sender=request.user).update(is_read=True)
    
    # Check if blocked
    from .models import BlockedUser
    other_participant = thread.participants.exclude(pk=request.user.pk).first()
    is_blocked = False
    if other_participant:
        is_blocked = BlockedUser.objects.filter(
            blocker=other_participant, blocked=request.user
        ).exists() or BlockedUser.objects.filter(
            blocker=request.user, blocked=other_participant
        ).exists()

    msgs = thread.messages.select_related("sender").order_by("created_at")
    if request.method == "POST":
        if is_blocked:
            messages.error(request, "You cannot send messages in this thread.")
            return redirect("messaging:thread", pk=thread.pk)
            
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg: Message = form.save(commit=False)
            msg.thread = thread
            msg.sender = request.user
            
            # Handle possible system/AI preset messages
            body_text = form.cleaned_data.get("body", "").strip()
            
            # If there's an image, or there's text
            if request.FILES.get("image") or body_text:
                if request.FILES.get("image"):
                    msg.image = request.FILES["image"]
                msg.save()
                
                ActivityLog.objects.create(user=request.user, action='message_sent', description=f"Sent a message inside a thread")
                thread.save(update_fields=["updated_at"])
                for u in thread.participants.exclude(pk=request.user.pk):
                    notify(
                        u,
                        f"New message from {request.user.email}",  # ✅ email not username
                        link=f"/messaging/thread/{thread.pk}/"
                    )
                    send_mail(
                        subject="New message on Findly",
                        message=f"You have a new message from {request.user.email} regarding an item. Log in to Findly to view and reply.",
                        from_email="findly@gmail.com",
                        recipient_list=[u.email],
                        fail_silently=True,
                    )
            return redirect("messaging:thread", pk=thread.pk)
    else:
        form = MessageForm()
        
    other_participant = thread.participants.exclude(pk=request.user.pk).first()
    is_online = False
    if other_participant and other_participant.last_seen:
        is_online = (timezone.now() - other_participant.last_seen).total_seconds() < 300

    return render(
        request,
        "messaging/thread.html",
        {
            "threads": get_user_threads(request.user),
            "active_thread": thread,
            "messages": msgs, 
            "form": form,
            "other_participant": other_participant,
            "is_online": is_online,
            "is_blocked": is_blocked
        }
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
    ActivityLog.objects.create(user=request.user, action='message_sent', description=f"Started a thread for item: {item.title}")
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


@login_required
@require_POST
def block_user(request, user_id: int):
    from .models import BlockedUser
    user_to_block = get_object_or_404(User, pk=user_id)
    if user_to_block == request.user:
        return JsonResponse({"error": "Cannot block yourself"}, status=400)
    
    blocked, created = BlockedUser.objects.get_or_create(blocker=request.user, blocked=user_to_block)
    if created:
        messages.success(request, f"You have blocked {user_to_block.first_name or user_to_block.email}.")
    else:
        blocked.delete()
        messages.success(request, f"You have unblocked {user_to_block.first_name or user_to_block.email}.")
    
    return redirect("messaging:inbox")


@login_required
@require_POST
def report_user(request, user_id: int):
    from .models import Report
    user_to_report = get_object_or_404(User, pk=user_id)
    thread_id = request.POST.get("thread_id")
    reason = request.POST.get("reason", "Inappropriate behavior")
    
    Report.objects.create(
        reporter=request.user,
        reported_user=user_to_report,
        thread_id=thread_id if thread_id else None,
        reason=reason
    )
    messages.success(request, "Report submitted successfully. We will review it shortly.")
    return redirect("messaging:inbox")
