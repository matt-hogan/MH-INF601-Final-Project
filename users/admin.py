from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminUserChange, AdminUserCreation
from .models import CustomUser


@admin.register(CustomUser)
class CustomerUserAdmin(UserAdmin):
    add_form = AdminUserCreation
    form = AdminUserChange
    model = CustomUser
    list_display = [ "email", 'first_name', 'last_name', "bookmakers" ]
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        ('Password', {'fields': ('old_password', 'new_password', 'new_password_confirm'), 'classes': ('collapse',)}),
        ('Sportbooks', {'fields': ('bookmakers',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'password_confirm')}),
        ('Sportbooks', {'fields': ('bookmakers',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    ordering = ('email',)
    search_fields = ('email',)
