from django.urls import path
from . import views

urlpatterns = [
 path('',  views.tracks, name='tracks'),
 path('track/<str:pk>/', views.singleTrack, name='single-track'),
 path('add-track/', views.addTrack, name='add-track'),
 path('edit-track/<str:pk>/', views.editTrack, name='edit-track'),
 path('delete-track/<str:pk>/', views.deleteTrack, name='delete-track'),
 path('assign-assessors/<str:pk>/', views.assignAssessors, name='assign-assessors'),
 path('task/<str:pk>/', views.singleTask, name='single-task'),
 path('add-task/<str:pk>/', views.addTask, name='add-task'),
 path('edit-task/<str:pk>/', views.editTask, name='edit-task'),
 path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),
 path('submit-task/<str:pk>/', views.submitTask, name='submit-task'),
 path('download-file/<str:pk>/', views.downloadFile, name = 'download-file'),
 path('admin-assessor-page/', views.adminAssessorPage, name='admin-assessor-page'),
 path('assessor-page/', views.assessorPage, name='assessor-page'),
 path('assessor-supervise/<str:pk>/', views.assessorSupervise, name='assessor-supervise'),
 path('assess-student-admin/<str:assessor>/<str:pk>/', views.assessStudentAdmin, name='assess-student-admin'),
 path('assess-student/<str:pk>/', views.assessStudent, name='assess-student'),
 path('assess-task-admin/<str:assessor>/<str:pk>/', views.assessTaskAdmin, name='assess-task-admin'),
 path('assess-task/<str:pk>/', views.assessTask, name='assess-task'),
 path('search-page/', views.searchPage, name='search-page'),
 path('add-category/', views.addCategory, name='add-category'),
 path('categories/', views.categories, name='categories'),
 path('edit-category/<str:pk>/', views.editCategory, name='edit-category'),
 path('delete-category/<str:pk>/', views.deleteCategory, name='delete-category'),
 path('download-certificate/<str:pk>/', views.downloadCertificate, name='download-certificate'),
]