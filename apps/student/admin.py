from django.contrib import admin
from .models import Student, Course, Subscription

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ("user","organization","course","is_student","membership_number","created","modified")
    list_filter = ("organization","is_student")
    readonly_fields = ('membership_number',)
    search_fields = ("user",)
    ordering = ("user",)


class CourseModelAdmin(admin.ModelAdmin):
    list_display = ("title","description","is_online","organization","created","modified")
    list_display_links = ("title","description",)



class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ("user","student","course","is_online","formatted_start_date","is_paid","formatted_end_date","created","modified")
    list_filter = ("student",)
    readonly_fields = ()

    # Override the save_model method to handle renew logic
    def save_model(self, request, obj, form, change):
        """
        Override save_model to create a new row if `is_paid` is checked.
        """
        if obj.is_paid and change:  # Only if is_paid is True and it's an existing subscription
            try:
                # Create a new subscription by renewing the current one
                obj.renew()
            except ValueError as e:
                self.message_user(request, str(e), level='error')
        else:
            super().save_model(request, obj, form, change)

    def formatted_start_date(self, obj):
        return obj.start_date.strftime('%d-%m-%Y')
    
    formatted_start_date.short_description = 'Start Date'
    
    def formatted_end_date(self, obj):
        return obj.end_date.strftime('%d-%m-%Y')
    
    formatted_end_date.short_description = 'End Date'
    

admin.site.register(Student,StudentModelAdmin)
admin.site.register(Course,CourseModelAdmin)
admin.site.register(Subscription,SubscriptionModelAdmin)