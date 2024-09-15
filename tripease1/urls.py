from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accountSetting/', views.accountSetting, name='accountSetting'),
    path('create/', views.creationForm, name='creationForm'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('login/', views.login, name='login'),
    path('login1/', views.login1, name='login1'),
    path('register/', views.register, name='register'),
]
