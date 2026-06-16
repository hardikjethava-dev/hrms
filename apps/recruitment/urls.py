from django.urls import path
from . import views

urlpatterns = [
    path('', views.recruitment_list, name='recruitment_list'),
    path('jobs/new/', views.job_create, name='job_create'),
    path('candidates/new/', views.candidate_manage, name='candidate_add'),
    path('candidates/<int:pk>/edit/', views.candidate_manage, name='candidate_edit'),
]
