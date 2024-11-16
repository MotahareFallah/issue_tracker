import datetime
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .managers import UserManager


class Section(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^09\d{9}$",
        message="Phone number must be entered in the format: '09111234567'. Up to 11 digits allowed.",
    )
    username = None
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    staff_member = models.BooleanField(default=False)
    active_member = models.BooleanField(default=False)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.is_staff and self.section is None:
            raise ValidationError("Section is required for staff members.")
        if not self.is_staff:
            self.section = None

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


def default_expires_at():
    return timezone.now() + datetime.timedelta(minutes=5)


class OtpCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expires_at)
    max_otp_try = models.IntegerField(default=5)
    otp_max_out = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

    def is_valid(self):
        return self.expires_at > timezone.now()


class OneTimeLink(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)
