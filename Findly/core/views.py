from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

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

        # Default role = user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            mobile=mobile,
            role="user"   # 👈 important
        )

        login(request, user)

        # Redirect based on role
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

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == "owner":
                return redirect("admin_dashboard")
            return redirect("user_dashboard")

        return render(request, "core/login.html", {
            "error": "Invalid credentials"
        })

    return render(request, "core/login.html")


# ==============================
# LOGOUT VIEW
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
    return render(request, "core/user_dashboard.html")


# ==============================
# OWNER DASHBOARD
# ==============================
@login_required
def owner_dashboard(request):
    if request.user.role != "owner":
        raise PermissionDenied
    return render(request, "core/admin_dashboard.html")

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboardView(request):
    if request.user.role == "owner":
        return redirect("admin_dashboard")
    else:
        return redirect("user_dashboard")