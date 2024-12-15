from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import User, Employee, Company

# Register User model with UserAdmin to manage it in the admin site
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'company', 'is_staff', 'is_active')
    list_filter = ('role', 'company', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

    # Add 'role' and 'company' to UserAdmin fieldsets for editing
    fieldsets = UserAdmin.fieldsets + (  # Add custom fields to UserAdmin
        ('Additional Info', {'fields': ('role', 'company')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (  # Add company when creating a user
        ('Additional Info', {'fields': ('role', 'company')}),
    )

# Register Employee model
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'training_status', 'date_joined', 'company', 'upload_employees_link')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('role', 'company', 'training_status')

    # Add a custom method to include the upload page link
    def upload_employees_link(self, obj):
        url = reverse('upload_employees')  # Reverse resolves the URL by its name
        return format_html('<a href="{}" target="_blank">Upload Employees</a>', url)

    upload_employees_link.short_description = "Upload Employees"

# Register Company model to manage it in admin site
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)
