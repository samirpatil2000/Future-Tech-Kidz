from django.db import models


class Franchisee(models.Model):

    name = models.CharField(max_length=30, default="Franchisee Name")
    owner = models.OneToOneField('account.Account', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='date of creation', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last date of update', auto_now=True)
    royalty_percentage = models.IntegerField(default=5, help_text='in percentage')

    def __str__(self):
        return self.name