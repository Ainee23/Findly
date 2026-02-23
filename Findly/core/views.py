from urllib import request

from django.shortcuts import render , redirect
from .forms import UserSignupForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def usersignupView(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request,'core/signup.html',{'form':form})

@login_required
def dashboard_redirect(request):
    if request.user.role == 'ADMIN':
        return redirect('/admin/')
    return redirect('user_dashboard')


@login_required
def user_dashboard(request):
    return render(request, 'core/user_dashboard.html')