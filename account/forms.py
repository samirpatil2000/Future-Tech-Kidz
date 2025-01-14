from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account, Student
from phonenumber_field.formfields import PhoneNumberField


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email' , 'password1', 'password2', )



class CreateStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('email', 'first_name', 'last_name', 'school_name')


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('email', 'first_name', 'last_name', 'school_name')

    def save(self, commit=False):
        object = self.instance
        object.email = self.instance.email
        object.first_name = self.instance.first_name
        object.last_name = self.instance.last_name
        object.school_name = self.instance.school_name
        if commit:
            object.save()
        return object

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")



