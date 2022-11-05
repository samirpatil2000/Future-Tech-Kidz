from django.db import models

class Enrollment(models.Model):

    student = models.ForeignKey("account.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(verbose_name='date of enrollment', auto_now_add=True)
