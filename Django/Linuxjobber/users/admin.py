from django.contrib import admin
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
	list_display = ['email', 'username', 'role', 'pwd_reset_token', 'allowed_project']

admin.site.register(CustomUser, CustomUserAdmin)
