from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student_list/', views.student_list, name='student_list'),
    # path('add_student/', views.add_student, name="add_student"),
    path('students/franchisee/<int:franchise_id>/', views.student_by_franchise, name="student_by_franchise"),
    path('students/courses/<int:course_id>/', views.student_by_course, name="student_by_course"),
]