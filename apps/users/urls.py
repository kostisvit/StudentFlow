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
    path('users/staff/new', UserStaffCreateView.as_view(), name='staff_new'),
    #path('users/student/new/', StudentUserCreateView.as_view(), name='student_new' ),
    path('users/student/<int:pk>/edit/', UserStaffUpdateView.as_view(), name='user_student_edit'),
    path('users/student/<int:pk>/delete/', views.fake_view,  name='user_student_delete'),
    # path('users/members/export', views.Export_data, name='members_list_export'),
    # path('users/member/dashboard/<int:pk>/', CustomUserDashboardView.as_view(), name='member_dashboard'),
    # path('users/password_change/', views.password_change, name='password_change'), 
    # path('users/ajax/user_search/', views.ajax_user_search, name='ajax_user_search'),
    # #upload file
    # path('users/upload_files/', upload_files, name='upload_files'),
    path('users/documents', DocumentListView.as_view(), name='document_list'),
    # path('users/files/delete/<int:pk>/', UserFileDeleteView.as_view(), name='user_file_delete'),
]