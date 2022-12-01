from django import forms


from course.models import Enrollment, Transaction



class EnrollStudentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ('course',)


class UpdateEnrollStudentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = ('course', 'url')

    def save(self, commit=False):
        obj = self.instance
        obj.course = self.instance.course
        obj.url = self.instance.url
        if commit:
            obj.save()
        return obj


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('reference', 'amount')

class UpdateTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('reference', 'amount')

    def save(self, commit=False):
        obj = self.instance
        obj.reference = self.instance.reference
        obj.amount = self.instance.amount
        if commit:
            obj.save()
        return obj
