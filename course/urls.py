from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enrollments/', views.get_enrollments, name='enrollments'),

    path('students/franchisee/<int:franchise_id>/', views.student_by_franchise, name="student_by_franchise"),
    path('students/courses/<int:course_id>/', views.student_by_course, name="student_by_course"),


    path('students/add/', views.add_student, name="add_student"),
    path('students/', views.get_students, name="students"),
    path('enrollments/add/<int:student_id>', views.add_enrollment, name='enroll_student'),
    path('enrollments/update/<int:enrollment_id>', views.update_enrollment, name='update_enrollment'),
    path('enrollments/delete/<int:id>', views.delete_enrollment, name='delete_enrollment'),

    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<int:enrollment_id>', views.add_transactions, name='add_transaction'),
]