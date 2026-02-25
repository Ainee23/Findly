# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignupForm  # <-- Add this import

def usersignupView(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserSignupForm()
    
    return render(request, 'core/signup.html', {'form': form})