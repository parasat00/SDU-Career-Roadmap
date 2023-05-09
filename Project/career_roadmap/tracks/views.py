from django.shortcuts import render,redirect
from django.http import FileResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Track, Task, MultipleImage, Task_performance, Track_assessor, Task_assessor, Category, Track_review, Certificate
from .forms import TrackForm, TaskForm, TaskSubmitForm, TaskAssessForm, CategoryForm
from user.models import Profile, CustomUser
from .decorators import authorOrAdminOnly, allowed_groups
from operator import itemgetter
from .utils import submitTask, startTask, setStatus, createTaskPerformances, setPrerequisite, deleteTasks, deleteTask, createMarkdownImages, setTasksOrder, updatePrerequisites, searchPageLogic, paginatorLogic, certificateLogic, downloadCertificate

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def categories(request):
    categories = Category.objects.all()
    context = {'categories':categories, 'page_title':'categories'}
    return render(request, 'tracks/categories.html', context)


@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def editCategory(request,pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    if request.method=='POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    context = {'form':form}
    return render(request, 'tracks/formCategory.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def deleteCategory(request,pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('categories')


@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def addCategory(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New category has been successfully added')
            return redirect('categories')
    
    context = {'page_title':'add-category', 'form':form}
    return render(request, 'tracks/formCategory.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def adminAssessorPage(request):
    results = []
    assessors = CustomUser.objects.prefetch_related('profile').filter(groups__name='assessor')
    for assessor in assessors:
        task_assessors = Task_assessor.objects.select_related("task_performance").filter(~Q(task_performance=None), track_assessor__profile__user = assessor).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))
        results.append(
            {
                'assessor':assessor.profile,
                'completed':task_assessors.filter(task_performance__status='completed').count(),
                'waiting':task_assessors.filter(task_performance__status='waiting').count(),
            }
        )
    results, page_range = paginatorLogic(request, results, 10)
    
    context = {'page_title':'assessor-page','results':results, 'page_range':page_range}
    return render(request, 'tracks/adminAssessorPage.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin'])
def assessorSupervise(request, pk):
    assessor = Profile.objects.get(id=pk)
    students = []
    results = []
    
    task_assessors = Task_assessor.objects.select_related("task_performance").filter(~Q(task_performance=None), track_assessor__profile = assessor).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))
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
    
    results.sort(key=itemgetter('waiting'),reverse=True)
    results, page_range = paginatorLogic(request, results, 10)
    context = {'page_title':'assessor-page','results':results, 'page_range':page_range, 'assessor':assessor}
    return render(request, 'tracks/assessorPage.html', context)


@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'assessor'])
def assessorPage(request):
    assessor = request.user.profile
    students = []
    results = []
    
    task_assessors = Task_assessor.objects.select_related("task_performance").filter(~Q(task_performance=None), track_assessor__profile = assessor).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))
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
    
    results.sort(key=itemgetter('waiting'),reverse=True)
    results, page_range = paginatorLogic(request, results, 10)
    context = {'page_title':'assessor-page','results':results, 'page_range':page_range}
    return render(request, 'tracks/assessorPage.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'assessor'])
def assessStudent(request, pk):
    track_containers=[]
    profile = Profile.objects.get(id=pk)
    assessor = request.user.profile

    task_assessors =Task_assessor.objects.filter(track_assessor__profile=assessor, task_performance__profile=profile).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))
    
    tracks = task_assessors.values_list('track_assessor__track', flat=True).distinct()

    tasks = Task_performance.objects.filter(id__in=task_assessors.values_list('task_performance'))

    for track in tracks :

        tr = Track.objects.get(id=track)
        t = tasks.filter(track=tr)
        track_containers.append({
            'track':tr,
            'tasks': t,
            'completed':t.filter(status="completed").count(),
            "waiting":t.filter(status = 'waiting').count(),
        })
    context = {'track_containers':track_containers, 'profile':profile, 'page_title':'assessor-page'}
    return render(request, 'tracks/assessStudent.html',context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'assessor'])
def assessStudentAdmin(request, assessor, pk):
    track_containers=[]
    profile = Profile.objects.get(id=pk)
    assessor = Profile.objects.get(id= assessor)

    task_assessors =Task_assessor.objects.filter(track_assessor__profile=assessor, task_performance__profile=profile).filter(Q(task_performance__status = 'waiting')|Q(task_performance__status = 'completed'))
    
    tracks = task_assessors.values_list('track_assessor__track', flat=True).distinct()

    tasks = Task_performance.objects.filter(id__in=task_assessors.values_list('task_performance'))

    for track in tracks :

        tr = Track.objects.get(id=track)
        t = tasks.filter(track=tr)
        track_containers.append({
            'track':tr,
            'tasks': t,
            'completed':t.filter(status="completed").count(),
            "waiting":t.filter(status = 'waiting').count(),
        })
    context = {'track_containers':track_containers, 'profile':profile, 'assessor':assessor, 'page_title':'assessor-page'}
    return render(request, 'tracks/assessStudent.html',context)


@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'assessor'])
def assessTask(request, pk):
    user_task = Task_performance.objects.select_related("task","profile","track").get(id=pk)
    track = user_task.track
    task = user_task.task
    profile = user_task.profile

    bul = False
    form = TaskAssessForm(instance=user_task)
    if request.method=='POST':
        form = TaskAssessForm(request.POST, instance=user_task)
        if form.is_valid():
            user_task = form.save(commit=False)
            if request.POST['grade'] == 'passed':
                user_task.grade = 'passed'
                user_task.status = ('completed','Completed')[0]
                bul = True
                certificateLogic(profile, track)
            elif request.POST['grade'] == 'redo':
                user_task.grade = 'redo'
                user_task.status = ('inProgress', 'In Progress')[0]
            user_task.save()
            if bul: updatePrerequisites(task, profile)
            return redirect('assess-student', profile.id)
                
    context = {
        'task': task, 
        'form':form, 
        'track':track, 
        'user_task':user_task,
        'profile':profile
        }
    return render(request, 'tracks/assessTask.html', context)

@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'assessor'])
def assessTaskAdmin(request, assessor,pk):
    assessor_profile = Profile.objects.get(id = assessor)
    user_task = Task_performance.objects.select_related("task","profile","track").get(id=pk)
    track = user_task.track
    task = user_task.task
    profile = user_task.profile

    bul = False
    form = TaskAssessForm(instance=user_task)
    if request.method=='POST':
        form = TaskAssessForm(request.POST, instance=user_task)
        if form.is_valid():
            user_task = form.save(commit=False)
            if request.POST['grade'] == 'passed':
                user_task.grade = 'passed'
                user_task.status = ('completed','Completed')[0]
                bul = True
            elif request.POST['grade'] == 'redo':
                user_task.grade = 'redo'
                user_task.status = ('inProgress', 'In Progress')[0]
            user_task.save()
            if bul: updatePrerequisites(task, profile)
            return redirect('assess-student-admin', assessor , profile.id)
                
    context = {
        'task': task, 
        'form':form, 
        'track':track, 
        'user_task':user_task,
        'profile':profile,
        'assessor':assessor_profile,
        }
    return render(request, 'tracks/assessTask.html', context)

def tracks(request):
    tracks = Track.objects.all()
    mytracks = []
    if request.user.is_authenticated:
        profile = request.user.profile
        mytrackList = profile.my_tracks.all()
        tracks = Track.objects.exclude(id__in=mytrackList).prefetch_related('track_review_set')
        for t in mytrackList:
            user_tasks = t.task_performance_set.select_related('task').filter(profile=profile)
            total = user_tasks.count()
            completed = user_tasks.filter(status='completed').count()
            waiting = user_tasks.filter(status='waiting').count()
            mytracks.append(
                {
                    'track':t,
                    'tasks':user_tasks,
                    'total_tasks':total,
                    'waiting':waiting,
                    'completed':completed,
                    }
                )

    tracks_by_categories = []
    categories = Category.objects.all()
    
    for category in categories :
        cat_tracks = []
        for track in tracks.filter(category=category):
            rating = track.track_review_set.aggregate(Avg('rating'))['rating__avg']
            cat_tracks.append({'track':track, 'rating':rating})
        tracks_by_categories.append({'category':category, 'tracks':cat_tracks, 'count':len(cat_tracks)})

    tracks_by_categories.sort(key = itemgetter('count'), reverse = True)
    context = {
        'page_title':'tracks',
        'mytracks':mytracks,
        'tracks_by_categories':tracks_by_categories
        }
    return render(request, 'tracks/tracks.html', context)

def singleTrack(request, pk) :
    in_process = False    
    track = Track.objects.prefetch_related('track_review_set').get(id = pk)
# If user is authenticated and enrolled inside track dont show enroll button
    user = request.user
    user_tasks = None
    assessors = Track_assessor.objects.filter(track = track)
    rate_track = False
    show_certificate = False

    if user.is_authenticated:
        profile = user.profile
        if track in profile.my_tracks.all() :
            in_process = True
            user_tasks = Task_performance.objects.filter(profile=profile, track = track)
            tasks = track.task_set.all()

            if tasks.count() > user_tasks.count():
                createTaskPerformances(track, profile)
            
            tasks_completed = user_tasks.filter(status='completed').count()
            tasks_count = tasks.count()

            certified = False
            certificate = None
                
            try:
                certificate = profile.my_certificates.get(track=track)
            except:
                certified = True

            # If user completed all the tasks
            if tasks_completed == tasks_count and certified:
                show_certificate = True
            
            try :
                Track_review.objects.get(track=track, owner=profile)
            except Track_review.DoesNotExist:
                if user_tasks.filter(status="completed").exists() :
                    rate_track = True
        
    queryset = None
    if user_tasks is not None:
        queryset = user_tasks
    else :
        queryset = track.task_set.all()
    
    queryset, page_range = paginatorLogic(request, queryset, 21)


    rating = track.track_review_set.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        if "Enroll" in request.POST:
            track.students.add(profile)
            createTaskPerformances(track, profile)
            return redirect('single-track', pk) 
        elif "generate" in request.POST:
            certificateLogic(profile, track)
            return redirect('single-track', pk)
        elif "Rate" in request.POST:
            if 'rating' in request.POST:
                Track_review.objects.create(
                    track = track,
                    owner = profile,
                    body = request.POST['comment'],
                    rating = request.POST['rating'],
                )
                messages.success(request,'You have successfully rated the track!')
            else:
                messages.error(request, 'You cannot leave the rating empty')
            return redirect('single-track', pk)
    context = {
        'track':track,
        'in_process':in_process, 
        'queryset':queryset,
        'assessors':assessors,
        'rating':rating,
        'rate_track':rate_track,
        'page_range':page_range,
        'show_certificate':show_certificate,
        'certificate':certificate,
        }
    return render(request, 'tracks/singleTrack.html', context)




@login_required(login_url='login')
@allowed_groups(allowed_groups=['admin', 'creator'])
def addTrack(request):
    form = TrackForm()
    profile = request.user.profile
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            
            temp = form.save(commit=False)
            temp.author = profile
            temp.save()
            form.save_m2m()
            return redirect('assign-assessors', temp.id)

    context = {'form':form, 'method':'Add', 'page_title':'add-track'}
    return render(request, 'tracks/formTrack.html', context)

@login_required(login_url='login')
@authorOrAdminOnly
def assignAssessors(request, pk):
    track = Track.objects.get(id=pk)
    profiles = Profile.objects.filter(user__groups__name='assessor')
    if request.method == 'POST':
        for p_id in request.POST.getlist('profile'):
            profile = Profile.objects.get(id = p_id)
            try:
                Track_assessor.objects.get(track = track, profile = profile)
            except Track_assessor.DoesNotExist:
                a = Track_assessor.objects.create(track = track, profile = profile)
                a.save()
        return redirect('single-track', pk)

    context = {'profiles':profiles}
    return render(request, 'tracks/assignAssessors.html', context)

@login_required(login_url = 'login')
@authorOrAdminOnly
def editTrack(request, pk):
    track = Track.objects.get(id=pk)
    form = TrackForm(instance=track)

    if request.method == 'POST':
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            return redirect('tracks')

    context = {'form':form, 'method':'Save'}
    return render(request, 'tracks/formTrack.html', context)

@login_required(login_url='login')
@authorOrAdminOnly
def deleteTrack(request, pk):
    track = Track.objects.get(id=pk)
    deleteTasks(track, request)
    track.delete()
    return redirect('tracks')

def singleTask(request, pk) :
    if request.user.is_authenticated:
        profile = request.user.profile
    task = Task.objects.get(id = pk)
    track = task.track
    user_task = None
    if request.user.is_authenticated and track in request.user.profile.my_tracks.all():
        try: 
            user_task = Task_performance.objects.get(profile = profile, task=task,track=track)
        except Task_performance.DoesNotExist:
            return redirect('single-track', track.id)


    form = TaskSubmitForm(instance=user_task)
    prerequisites = []
    if request.user.is_authenticated and track in profile.my_tracks.all():
        for pr in task.prerequisite.all():
            prerequisites.append(pr.task_performance_set.get(profile=profile, track=track))
    else:
        for pr in task.prerequisite.all():
            prerequisites.append(pr)
    
    assessors = Track_assessor.objects.filter(track = track)
    assigned_assessors = []
    if request.method=='POST':
        
        if 'startTask' in request.POST:
            startTask(request, user_task)
            return redirect('single-task', pk)
        elif 'submitTask' in request.POST:
            submitTask(request, user_task,pk)


    dict_data = Task_performance.objects.filter(track=track, task=task).filter(~Q(status="blocked"), ~Q(status ="available"))
    dict = {
        "students":dict_data.count(),
        "taking":dict_data.filter(Q(status="inProgress") | Q(status="waiting")).count(),
        "completed":dict_data.filter(status="completed").count(),
    }
    
    assigned_assessors = Task_assessor.objects.prefetch_related('track_assessor').filter(task_performance=user_task)

    context = {
        'task': task, 
        'form':form, 
        'track':track, 
        'user_task':user_task, 
        'prerequisites':prerequisites,
        'assessors':assessors,
        'assigned_assessors':assigned_assessors,
        'data':dict,
        'students_num':dict_data.count(),
        }
    return render(request, 'tracks/singleTask.html', context)

@login_required(login_url='login')
@authorOrAdminOnly
def addTask(request,pk):
    track = Track.objects.get(id = pk)
    form = TaskForm(initial={'track':track})
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES,initial={'track':track})
        
        if form.is_valid():
            task = form.save(commit=False)
            task.track = track
            
            setTasksOrder(track, task)
            task.save()
            setPrerequisite(task, request)
            createMarkdownImages(request.FILES.getlist('images'), task)
            return redirect('single-track', pk)

    context = {
        'form':form, 
        'text':'Add', 
        'track':track,
        }
    return render(request, 'tracks/formTask.html', context)

@login_required(login_url='login')
@authorOrAdminOnly
def editTask(request, pk):
    task = Task.objects.select_related('track').get(id = pk)
    form = TaskForm(instance=task)
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        
        form = TaskForm(request.POST, request.FILES, instance=task)
        
        if form.is_valid():
            createMarkdownImages(request.FILES.getlist('images'), task)
            task = form.save()
            if task.track in profile.my_tracks.all():
                setStatus(profile,None,task)
            return redirect('single-track', task.track.id)
    images = MultipleImage.objects.filter(task=task)
    context = {
        'form':form, 
        'text':'Save', 
        'images':images, 
        'track':task.track,
        'other_tasks':task.track.task_set.exclude(id=task.id)}
    return render(request, 'tracks/formTask.html', context)

@login_required
def downloadFile(request, pk):
    user_task = Task_performance.objects.get(id = pk)
    file = user_task.submit_file
    return FileResponse(file, as_attachment=True)


def searchPage(request):
    arr, model, search = searchPageLogic(request)
    
    arr, page_range = paginatorLogic(request, arr, 28)
    
    context = {'containers':arr, 'model':model, 'page_range':page_range, 'search':search}
    return render(request, 'searchPage.html', context)