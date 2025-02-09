from django.db import models


class Franchisee(models.Model):

    name = models.CharField(max_length=30, default="Franchisee Name")
    owner = models.OneToOneField('account.Account', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='date of creation', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last date of update', auto_now=True)

    def __str__(self):
        return self.name