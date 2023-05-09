from django.contrib.auth.models import Group 
from django.shortcuts import render, redirect
from .models import Profile, CustomUser
from tracks.decorators import allowed_groups
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from tracks.decorators import unauthenticated_only
from .forms import CustomUserCreationForm, ProfileChangeForm
from .utils import paginatorLogic
import re

@never_cache
@unauthenticated_only
def loginUser(request) :
 if request.method == 'POST':
  email = request.POST['email']
  password = request.POST['password']
  try:
   user = CustomUser.objects.get(email = email)
  except:
   messages.error(request, 'Email doesnt exists')
  
  user = authenticate(request, email=email, password=password)
  if user is not None:
   login(request, user)
   return redirect('tracks')
  else:
   messages.error(request, 'Email or password is incorrect')
  
 return render(request, 'user/login_register.html', {'mode':'login'})

def logoutUser(request):
 logout(request)
 return redirect('login')

@never_cache
@unauthenticated_only
def registerUser(request):
 form = CustomUserCreationForm()

 if request.method=='POST':
  form = CustomUserCreationForm(request.POST)
  if form.is_valid():
    user = form.save(commit=False)
    user.save()
    
    messages.success(request, 'User Account has been created!')
    login(request, user)
    profile = Profile.objects.get(user = user)
    return redirect('edit-profile',profile.id)
  else:
    messages.error(request,'An error occured during registration')
 context = {'mode':'register', 'form':form}
 return render(request, 'user/login_register.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def profiles(request):
 profiles = Profile.objects.exclude(user=request.user)
 profiles, page_range = paginatorLogic(request, profiles, 15)
 context = {'profiles':profiles, 'page_title':'profiles', 'page_range':page_range}
 return render(request, 'user/profiles.html', context)

@login_required(login_url='login')
def profile(request, pk):
 profile = Profile.objects.get(id=pk)
 allowed = (profile == request.user.profile) or request.user.groups.filter(name='admin').exists()
 groups = None

 if request.user.groups.filter(name='admin'):
  groups=Group.objects.all()
  if request.method == 'POST':
    profile.user.groups.clear()
    group=Group.objects.get(name=request.POST['profile-group'])
    group.user_set.add(profile.user)
    return redirect('profile',profile.id)

 context = {'profile':profile, 'allowed':allowed, 'groups':groups}
 return render(request, 'user/profile.html', context)

@login_required(login_url='login')
def editProfile(request, pk):
  profile = Profile.objects.get(id = pk)
  form = ProfileChangeForm(instance=profile)
  bul = True

  if request.method == "POST":
    form = ProfileChangeForm(request.POST, request.FILES, instance=profile)
    email = request.POST['email']

    if CustomUser.objects.exclude(id=profile.user.id).filter(email = email).exists():
      messages.error(request, 'Email "{}" already taken!!!'.format(email))
      bul = False
    
    
    if form.is_valid() and bul:
      temp = form.save(commit=False)
      user = temp.user
      user.email = temp.email
      user.first_name = temp.first_name
      user.last_name = temp.last_name
      user.save()
      temp.save()
      return redirect('profile',pk)
    

  context = {'form':form}
  return render(request, 'user/profile_edit.html', context)

@login_required(login_url='login')
def deleteProfile(request, pk):
  profile = Profile.objects.get(id = pk)
  profile.delete()
  return redirect('register')
