from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    academic_info = models.JSONField(default=dict, blank=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username}'s Profile"

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    prediction_data = models.JSONField()
    is_flagged = models.BooleanField(default=False)
    correction = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    feedback_text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction by {self.user.username} at {self.timestamp}"
