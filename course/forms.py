from django import forms

from course.models import Enrollment


class EnrollStudentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ('course',)