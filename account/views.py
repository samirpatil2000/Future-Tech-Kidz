from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from account.forms import RegistrationForm, AccountAuthenticationForm, EditStudentForm  # , AccountUpdateForm

# Create your views here.
from account.models import Account, Student
from course.models import Franchisee


def index(request):
    return render(request,'account/home.html')


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    # return render(request, 'course/register.html', context)
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')



def login_view(request):
    context={}

    user=request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # return render(request, "course/login.html", context)
    return render(request, "account/login.html", context)

@login_required
def branch_profile(request):
    franchisee = get_object_or_404(Franchisee, owner=request.user.id)
    context = {
        "user": Account.objects.get(id=request.user.id),
        "franchisee": franchisee
    }
    return render(request, 'account/branch_profile.html', context=context)

#
@login_required
def update_student_profile(request):
    student_object = get_object_or_404(Student, id=request.user.id)
    form = EditStudentForm()
    if request.method == "POST":
        form = EditStudentForm(request.POST or None, instance=student_object)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            messages.success(request, "Profile Successfully Updated ..!")
            return redirect('student_profile')

    form = EditStudentForm(initial={
        "email": student_object.email,
        "first_name": student_object.first_name,
        "last_name": student_object.last_name,
        "school_name": student_object.school_name,
    })
    context = {
        'form': form
    }
    return render(request, 'account/student_profile.html', context=context)