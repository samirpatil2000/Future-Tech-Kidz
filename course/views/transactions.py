from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from course.forms import  TransactionForm, UpdateTransactionForm
from course.models import Enrollment, Franchisee, Transaction

from django.contrib.auth.decorators import login_required



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
def transactions_admin(request):
    if not request.user.is_superuser:
        messages.warning(request, "Not Authorized")
        return redirect('home')

    context = {
        "transactions": Transaction.objects.all()
    }
    return render(request, 'course/transactions_admin.html', context=context)




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