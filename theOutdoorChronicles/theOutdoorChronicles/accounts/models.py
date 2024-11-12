from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from theOutdoorChronicles.accounts.managers import AppUserManager
from theOutdoorChronicles.accounts.validators import validate_image_size


class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = AppUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    bio = models.TextField(
        null=True,
        blank=True
    )

    website = models.URLField(
        null=True,
        blank=True
    )

    social_media_account = models.URLField(
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        validators=[validate_image_size],
        null=True,
        blank=True
    )
