from . import Account
from django.db import models
from course.models import Transaction, Enrollment, Course
from django.db.models import Sum

class Student(Account):
    school_name = models.CharField(max_length=30, blank=True, null=True)
    franchisee_name = models.ForeignKey('course.Franchisee', on_delete=models.SET_NULL, blank=True, null=True)

    def enroll_course(self):
        return Enrollment.objects.filter(student_id=self.id).values('course_id')

    def __str__(self):
        return self.full_name

