from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


# ================= USER MANAGER =================

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have email")

        email = self.normalize_email(email)

        extra_fields.setdefault("role", "user")

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "owner")

        return self.create_user(email, password, **extra_fields)



# ================= USER =================

class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("user", "User"),
    )

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)

    last_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user"
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



# ================= FINDLY MODEL =================

class FindlyPlace(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    placeImage = models.ImageField(
        upload_to="findly_images/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name