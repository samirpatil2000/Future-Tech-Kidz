from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enrollements/', views.get_enrollments, name='student_list'),


    path('students/franchisee/<int:franchise_id>/', views.student_by_franchise, name="student_by_franchise"),
    path('students/courses/<int:course_id>/', views.student_by_course, name="student_by_course"),


    path('students/add/', views.add_student, name="add_student"),
    path('students/', views.get_students, name="students"),
]