from django.contrib import messages
from django.shortcuts import render, redirect
from course.models import Enrollment, Franchisee
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/index.html')


def index(request):
    return render(request, template_name='course/table.html')


def fetch_students(request, **kwargs):
    title = kwargs.get('title') and kwargs.pop('title')
    context = {
        "title": title,
        "enroll_students": Enrollment.objects.filter(**kwargs)
    }
    return render(request, template_name='course/student_list.html', context=context)


def student_list(request):
    return fetch_students(request)


def student_by_franchise(request, franchise_id):
    return fetch_students(request, student__franchisee_name_id=franchise_id, title="Students By Franchise")


def student_by_course(request, course_id):
    return fetch_students(request, course_id=course_id, title="Students By Course")


@login_required
def get_students(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists() :
        messages.warning(request, "User does not exists")
        return redirect('home')
    context = {
        'enroll_students': Enrollment.objects.filter(student__franchisee_name_id=franchise[0].id)
    }
    return render(request, template_name='course/student_list_br_franchise.html', context=context)


def add_student(request):
    context = {

    }
    return render(request, template_name='course', context=context)
