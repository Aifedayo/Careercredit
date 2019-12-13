from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('role',)}),

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username', 'role', 'pwd_reset_token','user_role']
	list_filter = ('user_role',)
	actions = ['update_role',]

	def update_role(self, request, queryset):
		try:
			for user in queryset:
				user.update_role()
			self.message_user(request,'{} user roles updated successfully'.format(queryset.count()),messages.SUCCESS)

		except:
			self.message_user(request,'Error updating user role',messages.ERROR)

	update_role.short_description = "Update selected user roles"




admin.site.register(CustomUser, CustomUserAdmin)
