from django.db import models
from datetime import timedelta
from django.utils import timezone
import uuid



class Status(models.Model):
    token = models.CharField(max_length=120)
    status = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.token

class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    telegram_name = models.CharField(max_length=120)

    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)

    invited = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    has_permission = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    subscription_date = models.DateTimeField(auto_now=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}"


def generate_unique_token():
    while True:
        token = uuid.uuid4()
        if not Invite.objects.filter(token=token).exists():
            return token


class Invite(models.Model):
    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="invites")
    receiver = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True, blank=True)

    role_choices = (
        ("admin", "admin"),
        ("user", "user"),
    )
    role = models.CharField(max_length=120, choices=role_choices)

    token = models.UUIDField(default=generate_unique_token, editable=False, unique=True)
    name = models.CharField(max_length=120, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.creator} {self.role}"

    @property
    def is_expired(self):
        return self.created + timedelta(minutes=10) < timezone.now()

def generate_unique_token_sub():
    while True:
        token = uuid.uuid4()
        if not Plan.objects.filter(token=token).exists():
            return token

class Plan(models.Model):
    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="plans")
    receiver = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True, blank=True)

    token = models.UUIDField(default=generate_unique_token_sub, editable=False, unique=True)
    days = models.IntegerField(default=1)

    is_active = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    activated = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.creator} {self.days}"

    @property
    def is_expired(self):
        return self.created + timedelta(minutes=10) < timezone.now()

    @property
    def has_expired(self):
        return self.created + timedelta(days=self.days) < timezone.now()

def generate_unique_token_token():
    while True:
        token = uuid.uuid4()
        if not Token.objects.filter(token=token).exists():
            return token


class Token(models.Model):
    creator = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name="tokens")
    token = models.UUIDField(default=generate_unique_token_token, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.creator.username}"
    @property
    def has_expired(self):
        return self.created + timedelta(minutes=10) < timezone.now()

    @classmethod
    def create_for_user(cls, user: TelegramUser, expires_in=10):
        """Create a one-time link valid for `expires_in` minutes."""
        expires_at = timezone.now() + timedelta(minutes=expires_in)
        return cls.objects.create(user=user, expires_at=expires_at)