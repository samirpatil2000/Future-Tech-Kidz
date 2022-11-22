from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student_list/', views.student_list, name='student_list')
]