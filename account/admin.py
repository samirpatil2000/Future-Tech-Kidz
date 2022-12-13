from django.contrib import admin
from .models import Account, Student
from django.contrib.auth.admin import UserAdmin





class AccountAdmin(UserAdmin):

	list_display = ('full_name', 'email','date_joined', 'last_login', 'is_admin', 'is_franchisee_user')

	search_fields = ('email', 'first_name')
	ordering = ('email', 'first_name')

	readonly_fields= ('date_joined', 'last_login')  #the fields that can't be change

	filter_horizontal = ()
	list_filter = ()
	fieldsets  = (
        (None, {'fields': ('email', 'password')}),
        ('General Info', {'fields': ('first_name', "last_name")}),
        ('Permissions', {'fields': ("is_admin", "is_franchisee_user")}),
    )
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'first_name', "last_name", 'is_admin'),
		}),
	)
    # add_fieldsets
	exclude = ("is_superuser", "is_staff")


# Register your models here.

from django.contrib.auth.models import Group

admin.site.unregister(Group)


admin.site.register(Account, AccountAdmin)
# admin.site.register(Student)

@admin.register(Student)
class CustomStudent(admin.ModelAdmin):
	list_display = ('full_name', 'date_joined', 'last_login', 'franchisee_name')
	exclude = ('is_admin', "is_franchisee_user", "is_staff", "is_superuser", "password")


