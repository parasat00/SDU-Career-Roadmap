from django.contrib import admin
from .models import Track, Task, MultipleImage, Task_performance, Track_assessor, Category, Task_assessor, Track_review, Certificate

admin.site.register(Track)
admin.site.register(Task)
admin.site.register(MultipleImage)
admin.site.register(Task_performance)
admin.site.register(Track_assessor)
admin.site.register(Task_assessor)
admin.site.register(Category)
admin.site.register(Track_review)
admin.site.register(Certificate)