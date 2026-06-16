from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('new/', views.asset_manage, name='asset_add'),
    path('<int:pk>/edit/', views.asset_manage, name='asset_edit'),
    path('allocate/', views.asset_allocate, name='asset_allocate'),
    path('allocate/<int:pk>/edit/', views.asset_allocate, name='allocation_edit'),
]
