from django.urls import path
from django import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('students/franchisee/<int:franchise_id>/', views.student_by_franchise, name="student_by_franchise"),
    path('students/enrollments/', views.enrolled_courses, name="enrolled_courses"),

    path('students/', views.get_students, name="students"),
    path('students/add/', views.add_student, name="add_student"),
    path('students/update/<int:student_id>', views.update_student, name="update_student"),


    path('enrollments/', views.get_enrollments, name='enrollments'),
    path('enrollments/add/<int:student_id>', views.add_enrollment, name='enroll_student'),
    path('enrollments/update/<int:enrollment_id>', views.update_enrollment, name='update_enrollment'),
    path('enrollments/delete/<int:id>', views.delete_enrollment, name='delete_enrollment'),

    path('transactions/', views.transactions, name='transactions'),
    path('admin-transactions/', views.transactions_admin, name='transactions_admin'),
    path('transactions/<int:enrollment_id>', views.add_transactions, name='add_transaction'),
    path('transactions/update/<int:transaction_id>', views.update_transactions, name='update_transactions'),
    path('transactions/delete/<int:transaction_id>', views.delete_transactions, name='delete_transactions'),

]