from django import template
from tracks.models import Track

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
 return user.groups.filter(name=group_name).exists() 

@register.filter(name='is_author') 
def is_author(user, pk):
 return Track.objects.filter(id = pk, author = user.profile).exists()
