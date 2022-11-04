from . import Account
from django.db import models

class Student(Account):

    school_name = models.CharField(max_length=30)
    franchisee_name = models.ForeignKey('course.Franchisee', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def total_fees(self):

        return