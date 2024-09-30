from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Document, Vacation
from student.models import Student
from .forms import UserCreationForm, UserChangeForm


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'
    fk_name = 'user'

class UserAdmin(UserAdmin):
    inlines = (StudentInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)
    
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active','gender','is_company_owner','organization')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('organization','first_name', 'last_name', 'date_of_birth','phone_number','postal_code','address','city','country','gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_company_owner','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('organization','first_name', 'last_name', 'email',  'is_staff', 'is_student','is_active','is_company_owner','date_of_birth','phone_number','address','city','country','gender','postal_code','groups', 'user_permissions')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class VacationsAdmin(admin.ModelAdmin):
    readonly_fields = ('days',)  # Make 'days' read-only
    list_display = ('user', 'start_date', 'end_date', 'days')

admin.site.register(User, UserAdmin)
admin.site.register(Document)
admin.site.register(Vacation,VacationsAdmin)


