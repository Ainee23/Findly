from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "owner":
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper


def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "user":
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper