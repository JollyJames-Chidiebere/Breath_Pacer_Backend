from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        # Use the username from AbstractUser
        return self.username or (self.email or "user")

class BreathPlan(models.Model):
    """Reusable breathing patterns (e.g., 4-0-6-0)."""
    name = models.CharField(max_length=80, unique=True)
    inhale_ms = models.PositiveIntegerField()
    hold_ms   = models.PositiveIntegerField(default=0)  # hold after inhale
    exhale_ms = models.PositiveIntegerField()
    exhale_hold_ms = models.PositiveIntegerField(default=0)  # hold after exhale
    is_public = models.BooleanField(default=True)
    notes     = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.inhale_ms}-{self.hold_ms}-{self.exhale_ms}-{self.exhale_hold_ms})"

class BreathingSession(models.Model):
    """One user session using an optional plan."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions")
    plan = models.ForeignKey(BreathPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions")
    duration_seconds = models.PositiveIntegerField()  # total session duration
    inhale_seconds   = models.PositiveIntegerField()
    hold_seconds     = models.PositiveIntegerField(default=0)  # hold after inhale
    exhale_seconds   = models.PositiveIntegerField()
    exhale_hold_seconds = models.PositiveIntegerField(default=0)  # hold after exhale
    created_at = models.DateTimeField(auto_now_add=True)
    synced_at = models.DateTimeField(auto_now=True)     
    device     = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Session {self.id} for {self.user.username}"

class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress")
    total_sessions = models.PositiveIntegerField(default=0)
    total_minutes  = models.PositiveIntegerField(default=0)
    last_session   = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.user.username}'s progress"