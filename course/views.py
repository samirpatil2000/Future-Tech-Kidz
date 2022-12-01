from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import CreateStudentForm, EditStudentForm
from course.forms import EnrollStudentForm, TransactionForm, UpdateEnrollStudentForm, UpdateTransactionForm
from course.models import Enrollment, Franchisee, Transaction

from django.contrib.auth.decorators import login_required
# Create your views here.
from account.models import Account, Student


def home(request):
    return render(request, template_name='course/new_index.html')

def fetch_enrollments(request, **kwargs):
    title = kwargs.get('title') and kwargs.pop('title')
    context = {
        "title": title,
        "enroll_students": Enrollment.objects.filter(**kwargs)
    }
    return render(request, template_name='course/students.html', context=context)


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
        'enrollments': Enrollment.objects.filter(student__franchisee_name_id=franchise[0].id, is_active=True)
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
    return render(request, template_name='course/students.html', context=context)


def create_username(email: str):
    return email.split("@")[0]



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

        # else:
        #     messages.warning(request, "Something went wrong")
        #     return redirect('home')


    context = {
        'title': "Add New Student",
        'form': student_create_form
    }
    return render(request, template_name='course/student_create_form.html', context=context)

@login_required
def update_student(request, student_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchisee = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchisee.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')
    student_object = get_object_or_404(Student, id=student_id)
    if student_object.franchisee_name_id != franchisee[0].id:
        messages.warning(request, "Not Authorized to Student Details")
        return redirect('home')
    form = EditStudentForm()
    if request.method == "POST":
        form = EditStudentForm(request.POST or None, instance=student_object)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('students')

    form = EditStudentForm(initial={
        "email":student_object.email,
        "first_name":student_object.first_name,
        "last_name":student_object.last_name,
        "school_name":student_object.school_name,
    })
    context = {
        'title': "Update Student Details",
        'form': form
    }
    return render(request, template_name='course/student_create_form.html', context=context)

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


@login_required
def transactions(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')

    context = {
        "transactions": Transaction.objects.filter(enrollment__student__franchisee_name_id=franchise[0].id)
    }
    return render(request, 'course/transactions.html', context=context)

@login_required
def add_transactions(request, enrollment_id):
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

    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST or None)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.enrollment_id = enrollment_id
            transaction.created_by_id = request.user.id
            transaction.save()
            messages.success(request, "Transaction has Been Created Successfully..!")
            return redirect('transactions')

    context = {
        'form': form,
        'enrollment': enrollment
    }
    return render(request, 'course/add_transaction.html', context=context)


@login_required
def update_transactions(request, transaction_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')

    transaction = get_object_or_404(Transaction, pk=transaction_id)

    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST or None, instance=transaction)
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            messages.success(request, "Object Updated Successfully..!")
            return redirect('transactions')

    form = UpdateTransactionForm(initial={
        "reference": transaction.reference,
        "amount": transaction.amount
    })

    context = {
        'title': "Update Transaction",
        'form': form,
        'enrollment': transaction.enrollment,
        'transaction_id': transaction.id
    }
    return render(request, 'course/add_transaction.html', context=context)


@login_required
def delete_transactions(request, transaction_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('home')
    franchise = Franchisee.objects.filter(owner_id=request.user.id)
    if not franchise.exists():
        messages.warning(request, "User does not exists")
        return redirect('home')
    transaction  = get_object_or_404(Transaction, pk=transaction_id)
    transaction.delete()

    messages.success(request, "Object Deleted Successfully")
    return redirect('transactions')