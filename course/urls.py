from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]