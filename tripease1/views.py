from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TripForm
from django.db import IntegrityError

def index(request):
    return render(request, 'index.html')

def accountSetting(request):
    if request.method == 'POST':
        # Handle form submissions for updating user details
        # For simplicity, handling only email and phone updates here
        if 'update-email' in request.POST:
            email = request.POST.get('email')
            request.user.email = email
            request.user.save()
            messages.success(request, "Email updated successfully!")
        elif 'update-phone' in request.POST:
            phone = request.POST.get('phone')
            # Assuming you have a field for phone in your user profile model
            # request.user.profile.phone = phone
            # request.user.profile.save()
            messages.success(request, "Phone number updated successfully!")
        elif 'change-password' in request.POST:
            current_password = request.POST.get('current-password')
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Password updated successfully!")
                return redirect('login')  # Redirect to login after password change

    return render(request, 'accountSetting.html')

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
