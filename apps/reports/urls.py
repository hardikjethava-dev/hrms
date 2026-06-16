from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_dashboard, name='report_dashboard'),
    path('export/', views.export_report, name='export_report'),
    path('payslip/<int:pk>/', views.report_payslip, name='report_payslip'),
]
