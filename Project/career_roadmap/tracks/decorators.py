from django.shortcuts import redirect
from django.contrib import messages
from .models import Track, Task

def unauthenticated_only(view_function):
 def wrapper_function(request, *args, **kwargs):
  if request.user.is_authenticated:
   messages.error(request, 'You are already authenticated')
   return redirect('tracks')
  else:
   return view_function(request, *args, **kwargs)
 return wrapper_function

def allowed_groups(allowed_groups = []):
 def decorator(view_function):
  def wrapper_function(request, *args, **kwargs):
   groups = request.user.groups.all()
   for group_name in allowed_groups:
    if groups.filter(name=group_name).exists():
     return view_function(request, *args, **kwargs)
   
   messages.error(request, 'You are not authorized to this page')
   return redirect('tracks')
  
  return wrapper_function
 return decorator

def authorOrAdminOnly(view_function):
 def wrapper_function(request, *args, **kwargs):
  groups = request.user.groups.all()
  
  try:
   track = Track.objects.get(id = kwargs['pk'])
  except Track.DoesNotExist:
   track = Task.objects.select_related('track').get(id=kwargs['pk']).track
  
  if groups.filter(name='admin').exists() or track.author == request.user.profile:
   return view_function(request, *args, **kwargs)
  else:
   messages.error(request, 'You are not authorized to this page')
   return redirect('single-track', track.id)
 return wrapper_function