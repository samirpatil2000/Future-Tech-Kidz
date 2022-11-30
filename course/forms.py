from django import forms

from course.models import Enrollment, Transaction


class EnrollStudentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ('course',)


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('reference', 'amount')