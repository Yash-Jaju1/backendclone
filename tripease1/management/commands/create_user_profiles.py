from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from yourapp.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile instances for all users'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(f"Created UserProfile for {user.username}")
        if not users_without_profiles:
            self.stdout.write("All users already have a UserProfile.")
