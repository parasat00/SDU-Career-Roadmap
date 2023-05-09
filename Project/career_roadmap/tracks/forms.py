from django import forms
from django.forms import ModelForm
from .models import Track, Task, Task_performance, Category
from user.models import Profile
from django.db.models import Q

class TrackForm(ModelForm):
 class Meta:
  model=Track
  fields=['title', 'short_intro', 'content', 'category']
  widgets={
    'category':forms.CheckboxSelectMultiple(),
  }

class TaskForm(ModelForm):
 class Meta:
  model = Task
  fields = ['title', 'short_intro', 'content', 'prerequisite']
  widgets={
    'prerequisite':forms.CheckboxSelectMultiple(),
  }

 def __init__(self, *args, **kwargs):
    initial = kwargs.get('initial', {})
    super(TaskForm, self).__init__(*args, **kwargs)
    if self.instance.created is None:
      self.fields['prerequisite'].queryset = Task.objects.filter(~Q(id = self.instance.id), track = initial['track'])
    else:
      self.fields['prerequisite'].queryset = Task.objects.filter(~Q(id = self.instance.id), track = self.instance.track)

class TaskSubmitForm(ModelForm):
  class Meta:
    model = Task_performance
    fields = ['github_link', 'youtube_link', 'submit_file']
    labels = {
      'youtube_link':'Youtube link',
      'submit_file':'Your Job',
    }

class TaskAssessForm(ModelForm):
  class Meta:
    model=Task_performance
    fields = ['comment']

class CategoryForm(ModelForm):
  class Meta:
    model=Category
    fields = ['title']