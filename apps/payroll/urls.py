from django.urls import path
from . import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('generate/', views.generate_payroll_view, name='generate_payroll'),
    path('structure/new/', views.salary_structure_manage, name='salary_structure_add'),
    path('structure/<int:pk>/edit/', views.salary_structure_manage, name='salary_structure_edit'),
]
