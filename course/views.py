from django.contrib import messages
from django.shortcuts import render, redirect

from account.forms import CreateStudentForm
from course.models import Enrollment, Franchisee
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/index.html')


def index(request):
    return render(request, template_name='course/table.html')


def fetch_enrollments(request, **kwargs):
    title = kwargs.get('title') and kwargs.pop('title')
    context = {
        "title": title,
        "enroll_students": Enrollment.objects.filter(**kwargs)
    }
    return render(request, template_name='course/student_list.html', context=context)


def student_list(request):
    return fetch_enrollments(request)


def student_by_franchise(request, franchise_id):
    return fetch_enrollments(request, student__franchisee_name_id=franchise_id, title="Students By Franchise")


def student_by_course(request, course_id):
    return fetch_enrollments(request, course_id=course_id, title="Students By Course")


@login_required
def get_enrollments(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists() :
        messages.warning(request, "User does not exists")
        return redirect('home')
    context = {
        'enrollments': Enrollment.objects.filter(student__franchisee_name_id=franchise[0].id)
    }
    return render(request, template_name='course/enrollments.html', context=context)

@login_required
def get_students(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists() :
        messages.warning(request, "User does not exists")
        return redirect('home')
    context = {
        'students': Student.objects.filter(franchisee_name_id=franchise[0].id)
    }
    print(context)
    return render(request, template_name='course/students.html', context=context)


def student_details(request, id:int):
    return

def create_username(email: str):
    return email.split("@")[0]



@login_required
def add_student(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchisee = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchisee.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')
    student_create_form = CreateStudentForm()
    if request.method == "POST":
        student_create_form = CreateStudentForm(request.POST or None)
        if student_create_form.is_valid():
            student = student_create_form.save(commit=False)
            student.username = create_username(student.email)
            student.franchisee_name_id = franchisee[0].id
            student.set_password("1234")
            student.save()
            return redirect('home')

    context = {
        'form': student_create_form
    }
    return render(request, template_name='course/student_create_form.html', context=context)
