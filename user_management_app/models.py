from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from spa_app_core.validators import alphanumeric, phone_regex


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class UserRole(models.Model):
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role.strip()

    def delete_role(self, *args, **kwargs):
        users_with_role = UserData.objects.filter(role=self)

        for user in users_with_role:
            user.role = None
            user.save()

        super(UserRole, self).delete()


class UserData(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, validators=[alphanumeric], unique=True)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, validators=[alphanumeric], blank=True)
    last_name = models.CharField(max_length=150, validators=[alphanumeric], blank=True)
    phone_number = models.CharField(max_length=30, validators=[phone_regex])
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_username(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def delete_is_staff(self, *args, **kwargs):
        # check whether the user has lost the is_staff status
        if not self.is_superuser:
            self.is_staff = False
            self.role = None  # If so, set role to None
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
