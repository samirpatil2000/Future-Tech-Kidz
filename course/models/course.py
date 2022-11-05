from django.db import models

class Course(models.Model):

    title = models.CharField(max_length=30)
    description = models.TextField()
    duration = models.IntegerField(verbose_name="course duration (Months)")
    session = models.IntegerField(verbose_name="No of Sessions")
    fees = models.IntegerField()



