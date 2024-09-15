from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tripease1.models import UserProfile  # Replace 'yourapp' with your app name

class Command(BaseCommand):
    help = 'List all users and their profiles'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            try:
                profile = UserProfile.objects.get(user=user)
                self.stdout.write(f"{user.username} has a profile")
            except UserProfile.DoesNotExist:
                self.stdout.write(f"{user.username} does NOT have a profile")
