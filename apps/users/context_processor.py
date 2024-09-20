from .models import User
#from members.models import Member

def users_count(request):
    #user = request.user
    if request.user.is_authenticated:
        if request.user.is_superuser:
            organization = request.user.organization
            data = User.objects.filter(student__is_student=True).count()
        else:
            data = User.objects.filter(student__user__organization=request.user.organization,student__is_student=True).count()
        return {
            'users_count' : data
        }

    return {'users_count': None}
