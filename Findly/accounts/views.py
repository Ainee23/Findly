from django.contrib import messages
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, ProfileForm, RegisterForm

User = get_user_model()

import random
from django.core.mail import send_mail
from .models import EmailOTP
from .models import Profile
from items.models import Item, ClaimRequest
from reviews.models import Review


# ---------------- REGISTER ----------------

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # send otp for verification
            send_otp(user)

            # save user in session
            request.session["otp_user"] = user.id

            messages.success(request, "Account created! Please verify your email.")

            return redirect("accounts:verify_otp")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


# ---------------- SEND OTP ----------------

def send_otp(user):

    otp = str(random.randint(100000, 999999))
    
    # ✅ Add a highly visible print statement for local development
    print(f"\n=========================================")
    print(f"🔑 OTP FOR {user.email}: {otp}")
    print(f"=========================================\n")

    EmailOTP.objects.create(
        user=user,
        otp=otp,
    )

    try:
        send_mail(
            "Findly Login OTP",
            f"Your OTP is {otp}",
            None,
            [user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending OTP email: {e}")


# ---------------- LOGIN WITH OTP ----------------

class UserLoginView(LoginView):

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):

        user = form.get_user()

        # send otp
        send_otp(user)

        # save user in session
        self.request.session["otp_user"] = user.id

        return redirect("accounts:verify_otp")


# ---------------- VERIFY OTP ----------------

def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")

        user_id = request.session.get("otp_user")

        obj = EmailOTP.objects.filter(
            user_id=user_id,
            otp=otp,
            created__gte=timezone.now() - timedelta(minutes=10),
        ).last()

        if obj:

            user = obj.user

            login(request, user)

            messages.success(request, "Login successful")

            # redirect based on role
            if hasattr(user, "role") and user.role == "owner":
                return redirect("dashboard:admin_overview")

            return redirect("dashboard:home")

        else:
            messages.error(request, "Invalid OTP")

    return render(
        request,
        "accounts/verify.html",
    )


# ---------------- LOGOUT ----------------

class UserLogoutView(LogoutView):

    next_page = reverse_lazy("accounts:login")


# ---------------- PROFILE ----------------

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("accounts:profile")

    else:
        form = ProfileForm(
            instance=user
        )
        
    # User stats gathering
    items_posted = Item.objects.filter(owner=user).order_by("-created_at")
    my_claims = ClaimRequest.objects.filter(sender=user).order_by("-created_at")
    my_reviews = Review.objects.filter(reviewer=user).order_by("-created_at")
    
    stats = {
        'total_items': items_posted.count(),
        'total_claims': my_claims.count(),
        'total_reviews': my_reviews.count(),
    }

    return render(
        request,
        "accounts/profile.html",
        {
            "user": user,
            "form": form,
            "stats": stats,
            "items_posted": items_posted[:5],
            "my_claims": my_claims[:5],
            "my_reviews": my_reviews[:5],
        },
    )


# ---------------- PASSWORD CHANGE ----------------

class UserPasswordChangeView(PasswordChangeView):

    template_name = "accounts/password_change_form.html"

    success_url = reverse_lazy(
        "accounts:password_change_done"
    )


class UserPasswordChangeDoneView(
    PasswordChangeDoneView
):

    template_name = (
        "accounts/password_change_done.html"
    )
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def settings_view(request):

    user = request.user

    # ✅ create profile if missing
    profile_obj, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":

        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)

        user.save()

        if request.FILES.get("image"):
            profile_obj.image = request.FILES.get("image")
            profile_obj.save()

        messages.success(request, "✅ Profile updated!")

        return redirect("accounts:settings")

    return render(
        request,
        "accounts/settings.html",
        {
            "user": user,
            "profile": profile_obj,
        },
    )