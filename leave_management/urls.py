# leave_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_request_list, name='leave_request_list'),
    path('create/', views.create_leave_request, name='create_leave_request'),
    path('<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('<int:pk>/pdf/', views.download_leave_request_pdf, name='download_leave_request_pdf'),
]