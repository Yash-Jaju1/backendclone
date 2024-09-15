from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TripForm, UpdateEmailForm, UpdatePhoneForm, PasswordChangeCustomForm, NotificationPreferencesForm
from django.db import IntegrityError
from .models import UserProfile


def index(request):
    return render(request, 'index.html')

@login_required
def accountSetting(request):
    email_form = UpdateEmailForm(instance=request.user)
    phone_form = UpdatePhoneForm(instance=request.user.userprofile)
    password_form = PasswordChangeCustomForm(user=request.user)
    preferences_form = NotificationPreferencesForm(instance=request.user.userprofile)

    if request.method == 'POST':
        if 'update-email' in request.POST:
            email_form = UpdateEmailForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Email updated successfully!')
            else:
                messages.error(request, 'Error updating email.')
        
        elif 'update-phone' in request.POST:
            phone_form = UpdatePhoneForm(request.POST, instance=request.user.userprofile)
            if phone_form.is_valid():
                phone_form.save()
                messages.success(request, 'Phone number updated successfully!')
            else:
                messages.error(request, 'Error updating phone number.')
        
        elif 'change-password' in request.POST:
            password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Important!
                messages.success(request, 'Password changed successfully!')
            else:
                messages.error(request, 'Error changing password: {}'.format(password_form.errors.as_text()))
        
        elif 'update-preferences' in request.POST:
            preferences_form = NotificationPreferencesForm(request.POST, instance=request.user.userprofile)
            if preferences_form.is_valid():
                preferences_form.save()
                messages.success(request, 'Notification preferences updated successfully!')
            else:
                messages.error(request, 'Error updating preferences.')

    context = {
        'email_form': email_form,
        'phone_form': phone_form,
        'password_form': password_form,
        'preferences_form': preferences_form,
    }

    return render(request, 'accountSetting.html', context)

def creationForm(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            messages.success(request, "Trip created successfully!")
            return redirect('dashboard')
    else:
        form = TripForm()
    return render(request, 'creationForm.html', {'form': form})

def dashboard(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)

def itinerary(request):
    return render(request, 'itinerary.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard upon successful login
        else:
            # Handle login failure (e.g., show an error message)
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def login1(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('creationForm')  # Redirect to dashboard upon successful login
        else:
            # Handle login failure (e.g., show an error message)
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                if not UserProfile.objects.filter(user=user).exists():
                    UserProfile.objects.create(user=user)
                return redirect('login')
            except IntegrityError:
                form.add_error(None, "An error occurred while creating your profile. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
