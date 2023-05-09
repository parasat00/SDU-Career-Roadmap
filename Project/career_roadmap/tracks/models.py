from django.db import models
import uuid
from user.models import Profile, CustomUser

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Track(models.Model) :

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)

    students = models.ManyToManyField(Profile, blank=True, related_name='my_tracks')

    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    short_intro = models.CharField(max_length=300, null=True)

    category = models.ManyToManyField(Category, related_name='tracks', blank=False)

    def __str__(self) :
        return self.title

class Task(models.Model) :

    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    prerequisite = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.title

class Task_performance(models.Model):
    STATE_CHOICE = (('blocked', 'Not Available'), ('available', 'Available'), ('inProgress', 'In Progress'), ('waiting', 'Waiting'), ('completed','Completed'))
    GRADE_STATE = (('not-graded', 'Not Graded'), ('passed', 'Passed'), ('redo', 'Redo'))
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True, null=True)

    status = models.CharField(max_length=20, blank=True, null=True, choices=STATE_CHOICE, default=STATE_CHOICE[0][0])
    grade = models.CharField(max_length=20, blank=True, null=True, choices=GRADE_STATE, default=GRADE_STATE[0][0])

    comment = models.TextField(blank=True, null=True)

    youtube_link = models.CharField(max_length=500, null=True, blank=True)
    github_link = models.CharField(max_length=500, null=True, blank=True)
    submit_file = models.FileField(upload_to='uploads', blank=True, null=True)
    
    def __str__(self):
        return str(self.task.title)
class Certificate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(default='certificate_template.jpg', upload_to='uploads/certificates')
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_certificates')

    class Meta:
        ordering = ['-created']
        unique_together = [['owner', 'track']]

    def __str__(self):
        return str(self.track.title)

class Track_assessor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.track)
class Task_assessor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    track_assessor = models.ForeignKey(Track_assessor, on_delete=models.CASCADE, blank=True, null=True)
    task_performance = models.ForeignKey(Task_performance, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return str(self.task_performance)

class MultipleImage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='markdown_pics', blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

class Track_review(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        unique_together = [['owner', 'track']]