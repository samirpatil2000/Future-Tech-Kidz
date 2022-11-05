from . import Account
from django.db import models
from course.models import Transaction, Enrollment, Course
from django.db.models import Sum

class Student(Account):
    school_name = models.CharField(max_length=30)
    franchisee_name = models.ForeignKey('course.Franchisee', on_delete=models.SET_NULL, blank=True, null=True)

    def total_paid_amount(self, course_id):
        return Transaction.objects.filter(student__id=self.id, course_id=course_id).aggregate(Sum("amount")).get("amount__sum", 0)

    def remaining_amount(self, course_id):
        total_fees = Course.objects.get(course_id).Fees
        return total_fees - self.total_paid_amount(course_id)

    def enroll_course(self):
        return Enrollment.objects.filter(student_id=self.id).values('course_id')