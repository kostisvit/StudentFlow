from .models import CustomUser
#from members.models import Member

# def users_count(request):
#     #user = request.user
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             company = request.user.company
#             data = CustomUser.objects.filter(member__is_student=True).count()
#         else:
#             data = CustomUser.objects.filter(member__user__company=request.user.company,member__is_student=True).count()
#         return {
#             'users_count' : data
#         }

#     return {'users_count': None}
