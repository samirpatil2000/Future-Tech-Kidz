from django import template
from django.db.models import Sum

from course.models import Transaction, Course

register = template.Library()


def total_paid_amount(enrollment_id):
    return Transaction.objects.filter(enrollment_id=enrollment_id).aggregate(Sum("amount")).get(
        "amount__sum", 0) or 0

@register.simple_tag
def total_paid_amount_per_course(enrollment_id):
    return total_paid_amount(enrollment_id)

@register.simple_tag
def remaining_amount_per_course(enrollment_id, course_id):
    total_fees = Course.objects.get(id=course_id).fees or 0
    return total_fees - total_paid_amount(enrollment_id)