# from django.contrib import admin
# from .models import Department
#
# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('code','name','is_active','created_by')
#     readonly_fields = ('created_by',)
#     search_fields = ('code','name')
#     fieldsets = (
#         ('Department Details',{'fields':('code','name','is_active','created_by')}),
#     )