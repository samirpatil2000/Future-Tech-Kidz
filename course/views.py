from django.shortcuts import render


# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/index.html')


def index(request):
    return render(request, template_name='course/table.html')


def student_list(request):
    context = {
        {
            "name": "",
            "course_enrolled": "",
            "franchise": "",
            "fees_paid": 4500,
            "fees_pending": 1000
        }
    }
    student_list = Student.objects.filter()
    return render(request, template_name='course/student_list.html')
