from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.sessions.models import Session


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model) :
 id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
 created = models.DateTimeField(auto_now_add=True)

 user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
 first_name = models.CharField(max_length=100, blank=True, null=True)
 last_name = models.CharField(max_length=100, blank=True, null=True)
 email = models.EmailField(max_length=500, blank=True, null=True)
 short_intro = models.CharField(max_length=200, blank=True, null=True)
 about = models.TextField(blank=True, null=True)
 profile_image = models.ImageField(null=True, blank=True, upload_to='profile_pics/', default='profile_pics/user-default.png')
 social_linkedin = models.CharField(max_length=500, blank=True, null=True)
 social_instagram = models.CharField(max_length=500, blank=True, null=True)
 social_github = models.CharField(max_length=500, blank=True, null=True)
 phone_regex = RegexValidator(regex=r'^\+77(\d{9})$', message="Phone number must be entered in the format: '+77777777777'.")
 phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True) # Validators should be a list
 session_key = models.TextField(null=True)

 def __str__(self):
  return str(self.first_name)

 @property
 def is_logged_in(self):
    try:
        Session.objects.get(pk=self.session_key)
        return True
    except Session.DoesNotExist:
        return False
    return False
 class Meta:
    ordering = ['-created']