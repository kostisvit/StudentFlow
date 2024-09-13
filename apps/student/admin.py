from django.contrib import admin
from .models import Student, Course

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ("user","organization","is_student","membership_number","created","modified")
    list_filter = ("organization","is_student")
    readonly_fields = ('membership_number',)
    search_fields = ("user",)
    ordering = ("user",)


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ("title","description","is_online","organization","created","modified")
    list_display_links = ("title","description",)

admin.site.register(Student,StudentModelAdmin)
admin.site.register(Course,CourseModelAdmin)