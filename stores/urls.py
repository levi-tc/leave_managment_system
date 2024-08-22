from django.urls import path
from . import views

urlpatterns = [
    # ... your existing URL patterns ...
    path('create/', views.create_store, name='create_store'),
]