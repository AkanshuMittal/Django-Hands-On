"""
accounts/admin.py
WHY: Register your models in admin so you can manage users
     directly from /admin/ panel. Very useful during development.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmployerProfile, CandidateProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # What columns appear in the user list page
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter  = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Fields shown when editing a user
    fieldsets = (
        (None,            {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'bio', 'profile_photo')}),
        ('Role',          {'fields': ('role',)}),
        ('Permissions',   {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',         {'fields': ('date_joined',)}),
    )
    readonly_fields = ('date_joined',)

    # Fields shown when CREATING a new user from admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'company_size')
    search_fields = ('company_name', 'user__email')


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_job_title', 'experience_years')
    search_fields = ('user__email', 'skills')