from django.contrib import admin
from .models import Franchisee, Course, Transaction, Enrollment

admin.site.register(Franchisee)
admin.site.register(Course)
admin.site.register(Transaction)
admin.site.register(Enrollment)
# Register your models here.
