from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Profile, CustomUser
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
 if created:
  user = instance
  profile = Profile.objects.create(
   user = user,
   email = user.email, 
   first_name = user.first_name,
   last_name = user.last_name,
  )
  subject = 'Welcome to Career Roadmap platform'
  message = 'We are glad that you chose to join our platform!'
  send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER, 
    [profile.email],
    fail_silently=False,
  )

def deleteUser(sender, instance, **kwargs):
 user = instance.user
 user.delete()

def profileLoggedIn(sender, user, request, **kwargs):
  profile = user.profile
  profile.session_key = request.session.session_key
  profile.save()

def profileLoggedOut(sender, user, request, **kwargs):
  profile = user.profile
  profile.session_key = None
  profile.save()
  
post_save.connect(createProfile, sender=CustomUser)
post_delete.connect(deleteUser, sender=Profile)
user_logged_in.connect(profileLoggedIn)
user_logged_out.connect(profileLoggedOut)