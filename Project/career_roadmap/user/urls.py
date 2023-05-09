from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
 path('', views.loginUser, name='login'),
 path('logout/', views.logoutUser, name='logout'),
 path('register/', views.registerUser, name='register'),
 path('profiles/', views.profiles, name='profiles'),
 path('profile/<str:pk>/', views.profile, name='profile'),
 path('edit-profile/<str:pk>/', views.editProfile, name='edit-profile'),
 path('delete-profile/<str:pk>/', views.deleteProfile, name='delete-profile'),
]