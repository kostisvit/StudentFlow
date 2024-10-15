from import_export import resources, fields
from .models import Subscription,Student, Course
from import_export.widgets import ForeignKeyWidget

from users.models import User

class SubscriptionResource(resources.ModelResource):
    course = fields.Field(column_name='course',attribute='course',widget=ForeignKeyWidget(Course, 'title'))
    student = fields.Field(column_name='student', attribute='student', widget=ForeignKeyWidget(User, 'user__last_name'))
    
    class Meta:
        model = Subscription
        fields = ('student','course','start_date','end_date')
        export_order = ('student','course','start_date','end_date')
        widgets = {
            'start_date': {'format': '%d/%m/%Y'},
            'end_date': {'format': '%d/%m/%Y'},
        }


class StudentExportResource(resources.ModelResource):
    first_name = fields.Field(attribute="first_name",column_name="Όνομα",)
    last_name = fields.Field(attribute="last_name",column_name="Επώνυμο",)
    date_of_birth = fields.Field(attribute="date_of_birth",column_name="Ημ.Γένν.",)

    class Meta:
        model = Student
        fields = ('user__first_name', 'user__last_name', 'user__date_of_birth','user__email', 'user__phone_number', 'user__address','user__city','user__postal_code','user__country','user__gender', 'membership_date','user__is_active')
        export_order = ('first_name', 'last_name', 'date_of_birth','email', 'phone_number', 'address','city','postal_code','country','gender', 'membership_date','active')
        widgets = {
            'date_of_birth': {'format': '%d/%m/%Y'},
            'membership_date': {'format': '%d/%m/%Y'},
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request 
        
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset.filter(user__student__is_student=True)
            # Get the organization ID from the request user
            organization_id = self.request.user.organization.id
            return queryset.filter(
                user__student__is_student=True, 
                user__organization__id=organization_id
            )
        else:
            return queryset.none() 