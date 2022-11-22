from django.shortcuts import render
from course.models import Enrollment

# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/index.html')


def index(request):
    return render(request, template_name='course/table.html')


def student_list(request):
    context = {
        "enroll_students": Enrollment.objects.all()
    }
    return render(request, template_name='course/student_list.html', context=context)
