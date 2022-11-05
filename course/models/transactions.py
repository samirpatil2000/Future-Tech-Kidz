from django.db import models


class Transaction(models.Model):

    student = models.ForeignKey("account.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.SET_NULL, blank=True, null=True)
    paid_at = models.DateTimeField(verbose_name='date of enrollment', auto_now_add=True)
    reference = models.TextField()
    amount = models.IntegerField()

