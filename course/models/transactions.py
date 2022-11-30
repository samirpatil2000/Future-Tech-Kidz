from django.db import models


class Transaction(models.Model):

    enrollment = models.ForeignKey("course.enrollment", on_delete=models.SET_NULL, blank=True, null=True)
    paid_at = models.DateTimeField(verbose_name='date of payment', auto_now_add=True)
    created_by = models.ForeignKey("account.Account", on_delete=models.SET_NULL, blank=True, null=True)
    reference = models.TextField()
    amount = models.IntegerField()

