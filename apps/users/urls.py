from django.urls import path
from . import views
from .views import *
#from .views import CustomUserUpdateView, CustomUserCreateView,CustomUserDeleteView,CustomUserDashboardView,CustomUserStaffView,CustomUserStaffCreateView,password_change,ajax_user_search,upload_files,DocumentListView,custom_login_view,UserFileDeleteView


# Members defined as user (example users/export)

# def trigger_error(request):
#     division_by_zero = 1 / 0


urlpatterns = [
    path('accounts/login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    #path('sentry-debug/', trigger_error),
    path('users/staff', UserStaffView.as_view(), name='staff_list'),
    path('users/staff/vacations', VacationStaffListView.as_view(), name='vacations_list'),
    path('users/<int:pk>/edit/', views.staff_update, name='user_student_edit'),
    path('users/student/<int:pk>/delete/', views.fake_view,  name='user_student_delete'),
    path('users/export', views.Staff_export, name='staff_list_export'),
    # path('users/member/dashboard/<int:pk>/', CustomUserDashboardView.as_view(), name='member_dashboard'),
    path('users/password_change/', views.password_change, name='password_change'), 
    path('app/updates', views.fake_view, name='update_list'),
    # path('users/ajax/user_search/', views.ajax_user_search, name='ajax_user_search'),
    # #upload file
    path('users/upload_files/', student_upload_files, name='student_upload_files'),
    path('users/documents', DocumentListView.as_view(), name='student_document_list'),
    path('users/staff/upload_files/', views.staff_upload_files, name='staff_upload_files'),
    path('users/staff/documents', StaffDocumentListView.as_view(), name='staff_document_list'),
    # path('users/files/delete/<int:pk>/', UserFileDeleteView.as_view(), name='user_file_delete'),
]