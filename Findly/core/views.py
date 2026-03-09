from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings

from .forms import FindlyPlaceForm   # ✅ added
from .forms import UserForm          # ✅ added

User = get_user_model()


def homeView(request):
    return render(request, "core/home.html")


# ==============================
# SIGNUP VIEW
# ==============================
def usersignupView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        mobile = request.POST.get("mobile")

        if password != password2:
            return render(request, "core/signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "core/signup.html", {
                "error": "Email already exists"
            })

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            mobile=mobile,
            role="user"
        )

        login(request, user)

        if user.role == "owner":
            return redirect("admin_dashboard")

        return redirect("user_dashboard")

    return render(request, "core/signup.html")


# ==============================
# LOGIN VIEW
# ==============================
def userloginView(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "owner":
                return redirect("admin_dashboard")

            return redirect("user_dashboard")

        return render(
            request,
            "core/login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "core/login.html")


# ==============================
# LOGOUT
# ==============================
def userlogoutView(request):
    logout(request)
    return redirect("login")


# ==============================
# USER DASHBOARD
# ==============================
@login_required
def user_dashboard(request):

    if request.user.role != "user":
        raise PermissionDenied

    return render(
        request,
        "core/user_dashboard.html"
    )


# ==============================
# OWNER DASHBOARD
# ==============================
@login_required
def owner_dashboard(request):

    if request.user.role != "owner":
        raise PermissionDenied

    return render(
        request,
        "core/admin_dashboard.html"
    )


# ==============================
# AUTO DASHBOARD REDIRECT
# ==============================
@login_required
def dashboardView(request):

    if request.user.role == "owner":
        return redirect("admin_dashboard")

    return redirect("user_dashboard")


# ==============================
# REGISTER USER
# ==============================
def registerUser(request):

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save()

            email = form.cleaned_data['email']

            send_mail(
                subject="Welcome to Findly",
                message="Hello, Welcome to Findly",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect('login')

    else:
        form = UserForm()

    return render(
        request,
        'core/register.html',
        {'form': form}
    )


# ==============================
# CREATE PLACE (OWNER ONLY)
# ==============================
@login_required
def createPlace(request):

    if request.user.role != "owner":
        raise PermissionDenied

    if request.method == "POST":
        form = FindlyPlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.owner = request.user   # link place to owner
            place.save()
            return redirect("dashboard")
    else:
        form = FindlyPlaceForm()
        
    print("Rendering createPlace view for user:", request.user.email)
    return render(request, "core/create_place.html", {"form": form})