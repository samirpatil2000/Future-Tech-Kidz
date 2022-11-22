from django import template
from django.db.models import Sum

from course.models import Transaction, Course

register = template.Library()


def total_paid_amount(student_id, course_id):
    return Transaction.objects.filter(student__id=student_id, course_id=course_id).aggregate(Sum("amount")).get(
        "amount__sum", 0)

@register.simple_tag
def total_paid_amount_per_course(student_id, course_id ):
    return total_paid_amount(student_id, course_id)

@register.simple_tag
def remaining_amount_per_course(student_id, course_id):
    print("XXSS")
    total_fees = Course.objects.get(id=course_id).fees
    return total_fees - total_paid_amount(student_id, course_id)