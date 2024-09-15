from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    activity_type = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=50)
    accommodation = models.CharField(max_length=50)
    group_size = models.PositiveIntegerField()
    group_name = models.CharField(max_length=255)
    group_members = models.TextField()
    special_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Trip to {self.destination} by {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
