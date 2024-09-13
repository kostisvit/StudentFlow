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