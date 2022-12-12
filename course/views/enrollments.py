from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from course.forms import EnrollStudentForm, UpdateEnrollStudentForm
from course.models import Enrollment, Franchisee
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.models import Student





@login_required
def get_enrollments(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists() :
        messages.warning(request, "User does not exists")
        return redirect('home')
    context = {
        'enrollments': Enrollment.objects.filter(student__franchisee_name_id=franchise[0].id, is_active=True)
    }
    return render(request, template_name='course/enrollments.html', context=context)


@login_required
def add_enrollment(request, student_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    student = Student.objects.filter(id=student_id)
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists() or not student.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')

    form = EnrollStudentForm()
    if request.method == "POST":
        try:
            form = EnrollStudentForm(request.POST or None)
            if form.is_valid():
                enroll = form.save(commit=False)
                enroll.student_id = student_id
                enroll.save()
                messages.success(request, "Student has Been Enrolled Successfully..!")
        except Exception as e:
            messages.warning(request, "Can't create new enrollment for {}, cause, it already exists".format(student[0].full_name))
        return redirect('students')
    context = {
        'form': form,
        'student': student[0],
    }
    return render(request, template_name='course/enroll_student_form.html', context=context)


@login_required
def update_enrollment(request, enrollment_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')

    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')

    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    if enrollment.is_active == False:
        messages.warning(request, "Enrollment has been deleted..!")
        return redirect('enrollments')

    if request.method == "POST":
        form = UpdateEnrollStudentForm(request.POST or None, instance=enrollment)
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            messages.success(request, "Successfully Updated..!")
            return redirect('enrollments')

    form = UpdateEnrollStudentForm(initial={
        'course': enrollment.course,
        'url': enrollment.url
    })

    context = {
        'form': form,
        'student': enrollment.student,
        'enrollment_id':enrollment_id,
    }

    return render(request, template_name='course/enroll_student_form.html', context=context)

@login_required
def delete_enrollment(request, id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')
    enrollment  = get_object_or_404(Enrollment, pk=id)
    enrollment.is_active = False
    enrollment.save()

    messages.success(request, "Enrollment Deleted Successfully")
    return redirect('enrollments')
