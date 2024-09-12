from import_export import resources, fields
from .models import User
#from company.models import Company
from import_export.widgets import ForeignKeyWidget

class MemberResource(resources.ModelResource):
    first_name = fields.Field(attribute="first_name",column_name="Όνομα",)
    last_name = fields.Field(attribute="last_name",column_name="Επώνυμο",)
    date_of_birth = fields.Field(attribute="date_of_birth",column_name="Ημ.Γένν.",)
    #company = fields.Field(column_name='company_name',attribute='company',widget=ForeignKeyWidget(Company, 'name'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth','email', 'phone_number', 'address','city','postal_code','country','gender', 'membership_date','active','company')
        export_order = ('first_name', 'last_name', 'date_of_birth','email', 'phone_number', 'address','city','postal_code','country','gender', 'membership_date','active','company')
        widgets = {
            'date_of_birth': {'format': '%d/%m/%Y'},
            'membership_date': {'format': '%d/%m/%Y'},
        }
    
    # def get_queryset(self):
    #     current_user = self.user
    #     return CustomUser.objects.filter(company=current_user.company,member__is_student=True)