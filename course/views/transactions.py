from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from course.forms import TransactionForm, UpdateTransactionForm, LastActiveForm
from course.models import Enrollment, Franchisee, Transaction

from django.contrib.auth.decorators import login_required



@login_required
def transactions(request):
    if not request.user.is_franchisee_user and not request.user.is_admin:
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
    franchisee_id = request.GET.get("franchisee_id")
    order_by = int(request.GET.get("order_by", 1))
    to_date = request.GET.get("to_date")
    from_date = request.GET.get("from_date")


    kwargs = {}
    print("tt", to_date, from_date)

    franchisee = None

    if franchisee_id and franchisee_id != "x":
        franchisee = get_object_or_404(Franchisee, id=franchisee_id)
        kwargs["enrollment__student__franchisee_name_id"] = franchisee_id

    if to_date or from_date:
        if to_date and from_date:
            kwargs.update({
                "paid_at__gte" : from_date,
                "paid_at__lte" : to_date
            })
        else:
            messages.warning(request, "Please select to and from date")
            return redirect("transactions_admin")

    if not request.user.is_admin:
        messages.warning(request, "Not Authorized")
        return redirect('home')

    transactions = Transaction.objects.all().filter(**kwargs).order_by(("-" if order_by == -1 else "") + 'paid_at')
    print(transactions, "Transactions", kwargs)
    context = {
        "transactions": transactions,
        "selected_franchisee": franchisee,
        "franchisees": Franchisee.objects.all(),
        "order_by": order_by * -1,
        "form": LastActiveForm()
    }
    return render(request, 'course/transactions_admin.html', context=context)



@login_required
def add_transactions(request, enrollment_id):
    if not request.user.is_franchisee_user and not request.user.is_admin:
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
    if not request.user.is_franchisee_user and not request.user.is_admin:
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