from django.urls import path
from . import views

urlpatterns = [
    path('', views.performance_list, name='performance_list'),
    path('new/', views.performance_manage, name='performance_add'),
    path('<int:pk>/edit/', views.performance_manage, name='performance_edit'),
]
