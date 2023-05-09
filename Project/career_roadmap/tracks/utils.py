from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Track, Task, MultipleImage, Task_performance, Track_assessor, Task_assessor, Category, Track_review, Certificate
from .forms import TrackForm, TaskForm, TaskSubmitForm, TaskAssessForm
from user.models import Profile
from django.http import FileResponse
from django.db.models import Q
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from operator import itemgetter
from django.core.mail import send_mail
from django.conf import settings
from django.templatetags.static import static
from PIL import Image, ImageFont, ImageDraw 
from pathlib import Path
from django.core.files import File

@login_required
def downloadCertificate(request, pk):
  certificate = Certificate.objects.get(id = pk)
  
  s = certificate.file.path
  s = s[:s.find("jpg")]
  s = s+'pdf'

  img = Image.open(certificate.file.path)
  img = img.convert('RGB') 
  img.save(s, format="PDF")

  path = Path(s)
  file = File(path.open(mode="rb"), name=path.name)
  return FileResponse(file, as_attachment=True)

def certificateLogic(profile, track):
  tasks_taken = profile.task_performance_set.filter(status='completed', track=track).count()
  tasks_count = track.task_set.all().count()

  if tasks_taken == tasks_count:
    certificate = None
    try:
      certificate = Certificate.objects.get(owner = profile, track=track)
      
      original = certificate.file.path
      s = certificate.file.path
      s = s[:s.find("images")]
      url = str(s) + 'images\certificate_template.jpg'
      
      image = Image.open(url)
      owner_fullname = str(profile.first_name) +'-'+str(profile.last_name)
      author_fullname = str(track.author.first_name) + '-' + str(track.author.last_name)
      track_title = track.title

      font_size = 50
      title_font = ImageFont.truetype(s+'fonts/scriptmtbold.ttf',font_size)
      author_font = ImageFont.truetype(s+'fonts/scriptmtbold.ttf', 20)

      image = putText(track_title, title_font, (0,0,0), image, (0,185))
      image = putText(owner_fullname, title_font, (0,0,0), image, (0,300))
      image = putText(author_fullname, author_font, (0,0,0), image, (650,475), '')
      image = putText('Alimzhan Igenbayev', author_font, (0,0,0), image, (120,475), '')
      
      im = image.convert('RGB')
      
      url = str(s) + 'images/uploads/certificates/' + str(owner_fullname) + '-' + str(track_title) + '-' + str(author_fullname) + '.jpg'
      im=im.save(url)
      path = Path(url)
      with path.open(mode="rb") as f:
        certificate.file = File(f, name=path.name)
        certificate.save()
      os.remove(url)
      os.remove(original)
    except Certificate.DoesNotExist:
      certificate=Certificate.objects.create(
      owner=profile,
      track=track
      )
      
      s = certificate.file.path
      s = s[:s.find("images")]
      
      image = Image.open(certificate.file.path)
      owner_fullname = str(profile.first_name) +'-'+str(profile.last_name)
      author_fullname = str(track.author.first_name) + '-' + str(track.author.last_name)
      track_title = track.title

      font_size = 50
      title_font = ImageFont.truetype(s+'fonts/scriptmtbold.ttf',font_size)
      author_font = ImageFont.truetype(s+'fonts/scriptmtbold.ttf', 20)

      image = putText(track_title, title_font, (0,0,0), image, (0,185))
      image = putText(owner_fullname, title_font, (0,0,0), image, (0,300))
      image = putText(author_fullname, author_font, (0,0,0), image, (650,475), '')
      image = putText('Alimzhan Igenbayev', author_font, (0,0,0), image, (120,475), '')
      
      im = image.convert('RGB')
      
      url = str(s) + 'images/uploads/certificates/' + str(owner_fullname) + '-' + str(track_title) + '-' + str(author_fullname) + '.jpg'
      im=im.save(url)
      path = Path(url)
      with path.open(mode="rb") as f:
        certificate.file = File(f, name=path.name)
        certificate.save()
      os.remove(url)

def putText(message, font, fontColor, img, pos, mode='center'):
  image_editable = ImageDraw.Draw(img)  
  if mode == 'center':
    W, H = img.width, img.height  
    _, _, w, h = image_editable.textbbox((0, 0), message, font=font)
    image_editable.text(((W-w)/2, pos[1]), message, font=font, fill=fontColor)
  else: 
    image_editable.text(pos, message, font=font, fill=fontColor)
  return img

def sendNotification(student, assessors, task_title):
  subject = 'SDU Career Roadmap notification'
  for a in assessors:
    assessor = Profile.objects.get(id = a['track_assessor__profile'])
    count = Task_assessor.objects.filter(track_assessor__profile=assessor, task_performance__status = 'waiting').count()
    
    message = 'Task ' + task_title + ' was submitted by ' + str(student.first_name) + ' ' + str(student.last_name)+'\nOverall you have ' + str(count) + ' tasks to grade.'
    send_mail(
      subject,
      message,
      settings.EMAIL_HOST_USER, 
      [assessor.email],
      fail_silently=False,
    )

def paginatorLogic(request, queryset, elementsPerPage):
    page = request.GET.get('page')
    paginator = None
    paginator = Paginator(queryset, elementsPerPage)
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        page = 1
        queryset=paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        queryset = paginator.page(page)

    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1
    
    page_range = range(leftIndex, rightIndex)

    return queryset, page_range

def submitTask(request,user_task,pk):
 form = TaskSubmitForm(request.POST, request.FILES, instance=user_task)
 if form.is_valid():
  user_task = form.save(commit=False)
  user_task.status = ('waiting', 'Waiting')[0]
  user_task.save()
  assessors = user_task.task_assessor_set.filter(track_assessor__track = user_task.track).values('track_assessor__profile').distinct()
  sendNotification(user_task.profile, assessors, user_task.task.title)
  return redirect('single-task', pk)

def startTask(request, user_task):
 user_task.status = ('inProgress', 'In Progress')[0]
 user_task.save()
 assigned = request.POST.getlist('assessors')
 for a in assigned:
  a = Track_assessor.objects.select_related('track','profile').get(id = a)

  Task_assessor.objects.create(
   track_assessor = a,
   task_performance=user_task,
  )

def setStatus(profile, user_task = None, task=None):
 if user_task == None and task != None:
  user_task = Task_performance.objects.get(task=task, profile=profile, track=task.track)
    
 prerequisite_tasks = user_task.task.prerequisite.all()
 if user_task.status == 'blocked' and len(prerequisite_tasks) == 0:
  user_task.status = ('available', 'Available')[0]
    
 else:
  a = Task_performance.objects.filter(~Q(status = 'completed'), profile=profile, track = user_task.track, task__in=prerequisite_tasks)

  if a.count() > 0:
   user_task.status = ('blocked', 'Not Available')[0]
  elif a.count() == 0 and user_task.status == 'blocked':
   user_task.status = ('available', 'Available')[0]
    
 user_task.save()

#Create task-performances after user is enrolled
def createTaskPerformances(track, profile):
 for task in track.task_set.all():
  try:
   user_task = Task_performance.objects.get(task=task, profile=profile, track=track)
  except Task_performance.DoesNotExist:
   user_task = Task_performance.objects.create(
    task = task,
    profile = profile,
    track = track,
   )
  setStatus(profile, user_task)

def setPrerequisite(task, request):
 if 'prerequisite' in request.POST:
  bul = True
  for prerequisite in dict(request.POST)["prerequisite"]:
   pr = Task.objects.get(id = prerequisite)
   task.prerequisite.add(pr)

# delete every task in a track
def deleteTasks(track, request):
 tasks = Task.objects.filter(track = track)
 for task in tasks:
  deleteTask(request,task.id)

@login_required(login_url='login')
def deleteTask(request, pk):
 task = Task.objects.select_related('track').get(id = pk)
 id = task.track.id
 order = task.order
 prerequisites = []
 for pr in Task.objects.filter(prerequisite = task):
  prerequisites.append(pr)
  deleteMarkdownImages(task)
  fixOrders(order, task)
  # deleteSubmitFile(task)
  task.delete()
 for pr in prerequisites:
  setStatus(request.user.profile, None, pr)

 return redirect('single-track', id)

def deleteMarkdownImages(task):
 images = MultipleImage.objects.filter(task=task)

 for image in images:
  os.remove(image.image.path)

# fix the order number of the remaining tasks
def fixOrders(order, t):
 ordertasks = Task.objects.filter(track = t.track, order__gt = order).order_by('order')
 for ordertask in ordertasks:
  ordertask.order = ordertask.order - 1
  ordertask.save()

def deleteSubmitFile(task):
 if task.submit_file :
  os.remove(task.submit_file.path)

def createMarkdownImages(images, task):
 for image in images:
  MultipleImage.objects.create(image=image, task=task)

# set order to the task
def setTasksOrder(track, task):
 taskCount = Task.objects.filter(track=track).count()
 if taskCount == 0:
  task.order = 1
 else:
  task.order = taskCount + 1

# Function to update its prerequisites when the task is completed
def updatePrerequisites(task,profile):
 tasks = Task.objects.prefetch_related('prerequisite__task_performance_set').filter(prerequisite = task)
 for t in tasks:
  if t.prerequisite.count() == 1: 
   user_task = t.task_performance_set.get(profile = profile)
   user_task.status = ('available', 'Available')[0]
   user_task.save()
  else:
   prs = t.prerequisite.exclude(id = task.id)
   for pr in prs :
    a = pr.task_performance_set.filter(~Q(status = 'completed'), profile=profile)
    if a.count()==0:
     user_task = t.task_performance_set.get(profile = profile)
     user_task.status = ('available', 'Available')[0]
     user_task.save()

def searchPageLogic(request):
  search = ''
  if request.GET.get('search'):
    search = request.GET.get('search')
  
  model = request.GET.get('model')
  orderBy = request.GET.get('orderBy')
  arr = []

  if model == 'tracks':
    categories = Category.objects.filter(title__icontains = search)
    tracks = Track.objects.filter(
      Q(title__icontains=search)|
      Q(short_intro__icontains=search)|
      Q(category__in = categories)
      ).distinct().order_by(orderBy)
      
    
    for track in tracks:
      rating = track.track_review_set.aggregate(Avg('rating'))['rating__avg']
      arr.append({'track':track, 'rating':rating})
  elif model == 'tasks':
    user_tasks = []
    if request.user.is_authenticated:
      profile = request.user.profile
    
      user_tasks = profile.task_performance_set.filter(
        Q(task__title__icontains=search)|
        Q(task__short_intro__icontains=search)
      )
      if orderBy=='title':
        user_tasks = user_tasks.order_by('task__'+str(orderBy))
      else:
        user_tasks = user_tasks.order_by(orderBy)
    arr = arr + list(user_tasks)
    
    tasks = []

    if len(arr) > 0:
      exclude_tasks = list(user_tasks.values_list('task__id',flat=True))
      tasks = Task.objects.exclude(id__in = exclude_tasks)

    if len(tasks) == 0:
      tasks = Task.objects.filter(
        Q(title__icontains=search)|
        Q(short_intro__icontains=search)
        ).order_by(orderBy)
    else:
      tasks=tasks.filter(
        Q(title__icontains=search)|
        Q(short_intro__icontains=search)
        ).order_by(orderBy)
    
    arr = arr + list(tasks)
  elif model == 'assess-student':
    assessor = request.user.profile
    students = []
    results = []
    
    if orderBy == 'title':
      orderBy = '-task_performance__profile__first_name'
    
    task_assessors = Task_assessor.objects.select_related("task_performance").filter(~Q(task_performance=None), track_assessor__profile = assessor).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))

    task_assessors = task_assessors.filter(
      Q(task_performance__profile__first_name__icontains=search)|
      Q(task_performance__profile__last_name__icontains=search)|
      Q(task_performance__profile__email__icontains=search)|
      Q(task_performance__profile__short_intro__icontains=search)
    ).order_by(orderBy)
    
    for a in task_assessors:
        students.append(a.task_performance.profile)
    students = set(students)
    
    for student in students :
        results.append(
            {
                'student':student,
                'completed':task_assessors.filter(task_performance__profile=student, task_performance__status='completed').count(),
                'waiting':task_assessors.filter(task_performance__profile=student, task_performance__status='waiting').count(),
            }
        )
    arr = results
  
  elif model == 'users':
    if orderBy == 'title':
      orderBy = '-first_name'

    profiles = Profile.objects.filter(
      Q(first_name__icontains=search)|
      Q(last_name__icontains=search)|
      Q(short_intro__icontains=search)|
      Q(email__icontains=search)|
      Q(about__icontains=search)
      ).order_by(orderBy) 
    
    arr = profiles
  return arr, model,request.GET
