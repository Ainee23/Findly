from django import forms
from django.contrib.auth import get_user_model
from .models import FindlyPlace

User = get_user_model()


# ==========================
# USER FORM
# ==========================
class UserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User

        fields = [
            "email",
            "password",
            "first_name",
            "role",
        ]


# ==========================
# FINDLY PLACE FORM
# ==========================
class FindlyPlaceForm(forms.ModelForm):

    class Meta:
        model = FindlyPlace

        fields = [
            "name",
            "description",
            "placeImage",
        ]