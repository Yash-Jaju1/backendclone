from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Trip, UserProfile  # Ensure UserProfile is imported

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'contact_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    pass  # Add custom fields or methods if needed

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'start_date', 'end_date', 'budget', 'activity_type', 'cuisine', 'accommodation', 'group_size', 'group_name', 'group_members', 'special_notes']
