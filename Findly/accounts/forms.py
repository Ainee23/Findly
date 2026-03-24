from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()  # ✅ Use custom email-based User


class RegisterForm(forms.ModelForm):
    """Registration form using email + password (no username)."""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        min_length=8,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
        }

    # ✅ CHECK PASSWORD MATCH
    def clean(self):
        cleaned_data = super().clean()

        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data

    # ✅ PREVENT DUPLICATE EMAIL AND LOWERCASE IT
    def clean_email(self):
        email = self.cleaned_data.get("email").lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already registered"
            )

        return email

    # ✅ SAVE USER
    def save(self, commit=True):

        user = super().save(commit=False)
        user.email = user.email.lower()

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    """Login form using email (the core app uses email as USERNAME_FIELD)."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "Email address"}),
    )

    def clean(self):
        # Force email to lowercase before authenticating
        username = self.cleaned_data.get('username')
        if username:
            self.cleaned_data['username'] = username.lower()
            self.data = self.data.copy()
            self.data['username'] = username.lower()
        return super().clean()

from django.contrib.auth.forms import PasswordResetForm
class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        try:
            super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)
        except Exception as e:
            print(f"Error sending password reset email to {to_email}: {e}")


class ProfileForm(forms.ModelForm):
    """Update profile information."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "mobile"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "mobile": forms.TextInput(attrs={"placeholder": "Mobile number", "class": "form-control"}),
        }
