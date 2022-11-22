from django.shortcuts import render
from course.models import Enrollment

# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/index.html')

def index(request):
    return render(request, template_name='course/table.html')

def get_students(request, **kwargs):
    title = kwargs.get('title') and kwargs.pop('title')
    context = {
        "title": title,
        "enroll_students": Enrollment.objects.filter(**kwargs)
    }
    return render(request, template_name='course/student_list.html', context=context)

def student_list(request):
    return get_students(request)

def student_by_franchise(request, franchise_id):
    return get_students(request, student__franchisee_name_id=franchise_id, title="Students By Franchise")

def student_by_course(request, course_id):
    return get_students(request, course_id=course_id, title="Students By Course")


def add_student(request):
    context = {

    }
    return render(request, template_name='course', context=context)
