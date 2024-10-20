# urls.py
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('students/list', StudentListView.as_view(), name='students_list'),
    path('students/new/', StudentUserCreateView.as_view(), name='student_new' ),
    path('students/export', views.student_Export_data, name='students_list_export'),
    path('students/<int:pk>/update/', StudentUserUpdateView.as_view(), name='student_edit' ),
    #path('students/<int:pk>/delete/', StudentDeleteView.as_view(),  name='student_delete'),
    path('students/subscriptions/list', views.subscription_list_view, name='subscriptions_list'),
    path('students/subscriptions/export', views.subscriptions_export_data, name='subscriptions_list_export'),
    path('students/subscriptions/ends', views.expired_subscriptions_view, name='subscriptions_ends_list'),
    path('students/subscription/<int:pk>/update/', views.subscription_update_view, name='subscription_edit'),
    #path('students/subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    # path('students/course/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    #path('email-search/', EmailSearchView.as_view(), name='email_search'),
    path('students/courses/list', views.course_list_view, name='course_list'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course_edit' ),
]