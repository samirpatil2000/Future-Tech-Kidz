from django.contrib import admin
from .models import Franchisee, Course, Transaction, Enrollment



@admin.register(Franchisee)
class CustomFranchise(admin.ModelAdmin):
    list_display = ["name", "owner"]

    # def show_average(self, obj):
    #     from django.db.models import Avg
    #     result = Grade.objects.filter(person=obj).aggregate(Avg("grade"))
    #     return result["grade__avg"]



@admin.register(Course)
class CustomCourse(admin.ModelAdmin):
    list_display = ["title", "fees"]

@admin.register(Transaction)
class CustomTransaction(admin.ModelAdmin):
    list_display = [
        "student","course", "paid_at", "reference","amount",
    ]

@admin.register(Enrollment)
class CustomEnrollment(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled_at"]

