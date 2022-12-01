from django.db import models

class Enrollment(models.Model):

    student = models.ForeignKey("account.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(verbose_name='date of enrollment', auto_now_add=True)
    url = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student.first_name) + " | " + str(self.course.title)

    def save(self, *args, **kwargs):
        enrollment = Enrollment.objects.filter(student_id=self.student_id, course_id=self.course_id, is_active=True)
        if enrollment.exists() and enrollment[0].id != self.id:
            raise "Can't create new enrollment for {} cause, it already exists".format(self.student.full_name)

        return super().save(*args, **kwargs)