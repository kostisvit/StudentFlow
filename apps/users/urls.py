from django.urls import path
from .views import *
#from .views import CustomUserUpdateView, CustomUserCreateView,CustomUserDeleteView,CustomUserDashboardView,CustomUserStaffView,CustomUserStaffCreateView,password_change,ajax_user_search,upload_files,DocumentListView,custom_login_view,UserFileDeleteView


# Members defined as user (example users/export)

# def trigger_error(request):
#     division_by_zero = 1 / 0


urlpatterns = [
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    #path('sentry-debug/', trigger_error),
    # path('users/staff', CustomUserStaffView.as_view(), name='staff_list'),
    # path('users/staff/new', CustomUserStaffCreateView.as_view(), name='staff_new'),
    # path('users/member/new/', CustomUserCreateView.as_view(), name='member_new' ),
    # path('users/member/<int:pk>/edit/', CustomUserUpdateView.as_view(), name='member_edit'),
    # path('users/member/<int:pk>/delete/', CustomUserDeleteView.as_view(), name='member_delete'),
    # path('users/members/export', views.Export_data, name='members_list_export'),
    # path('users/member/dashboard/<int:pk>/', CustomUserDashboardView.as_view(), name='member_dashboard'),
    # path('users/password_change/', views.password_change, name='password_change'), 
    # path('users/ajax/user_search/', views.ajax_user_search, name='ajax_user_search'),
    # #upload file
    # path('users/upload_files/', upload_files, name='upload_files'),
    # path('users/documents', DocumentListView.as_view(), name='document_list'),
    # path('users/files/delete/<int:pk>/', UserFileDeleteView.as_view(), name='user_file_delete'),
]