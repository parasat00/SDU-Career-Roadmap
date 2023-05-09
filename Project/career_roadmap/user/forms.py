from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Profile

from django.forms import ModelForm

from django.forms.widgets import TextInput
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name",)
        labels = {
            "first_name":"First Name",
            "last_name":"Last Name"
        }
    
    


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class ProfileChangeForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image","first_name", "last_name", "short_intro", "about", "email", "social_linkedin", "social_instagram", "social_github", "phone_number"]
        widgets = {
            "phone_number": TextInput(attrs={'pattern': '^\+77(\d{9})$', 'title':'Phone number must be entered in the format: "+77777777777"', 'max':12}),
            "profile_image": forms.FileInput(attrs={"onchange":"loadFile(event)",})
        }
        labels = {
            "about":"ABOUT ME",
            "email":"Email address",
            "social_linkedin":"Linked in link",
            "social_instagram":"Instagram link",
            "social_github":"Github link",
        }

        def __init__(self, *args, **kwargs):
            super(ProfileChangeForm, self).__init__(*args, **kwargs)
            self.fields['phone_number'].widget.attrs.update({
                'pattern': '^\+77(\d{9})$'
            })
            
            for name, field in self.fields.items():
                field.widget.attrs.update({
                    'id': name
                })
