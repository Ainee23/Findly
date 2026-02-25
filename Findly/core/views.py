from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def usersignupView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Basic validation
        if not email or not password or not password2:
            error = "All fields are required."
            return render(request, 'core/signup.html', {'error': error})

        if password != password2:
            error = "Passwords do not match."
            return render(request, 'core/signup.html', {'error': error})

        if User.objects.filter(email=email).exists():
            error = "Email is already registered."
            return render(request, 'core/signup.html', {'error': error})

        # Create user
        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'core/signup.html')

def userloginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  # email auth
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': "Invalid credentials"})
    return render(request, 'core/login.html')

def userlogoutView(request):
    logout(request)
    return redirect('login')


def homeView(request):
    return render(request, 'core/home.html')


@login_required
def dashboardView(request):
    user = request.user

    if getattr(user, 'is_admin', False):  # check admin
        # Render admin dashboard
        return render(request, 'core/admin_dashboard.html')
    else:
        # Render user dashboard
        return render(request, 'core/user_dashboard.html')