# urls.py
from django.urls import path
from .views import StudentListView,StudentUserCreateView, SubscriptionListView, StudentUserUpdateView,CourseListView,SubscriptionEndsListView
#SubscriptionListView,SubscriptionCreateView,Export_data_subscription,courceview,delete_entry, SubscriptionUpdateView,SubscriptionDeleteView,compose_email,SubscriptionEndingListView
from . import views

urlpatterns = [
    path('students/list', StudentListView.as_view(), name='students_list'),
    path('students/new/', StudentUserCreateView.as_view(), name='student_new' ),
    path('students/<int:pk>/update/', StudentUserUpdateView.as_view(), name='student_edit' ),
    path('students/<int:pk>/delete/', views.fake_view,  name='student_delete'),
    path('students/subscriptions/list', SubscriptionListView.as_view(), name='subscriptions_list'),
    # path('students/subscriptions/export', views.Export_data_subscription, name='subscriptions_list_export'),
    #path('students/subscription/new', SubscriptionCreateView.as_view(), name='subscriptions_new'),
    path('students/subscriptions/ends', SubscriptionEndsListView.as_view(), name='subscriptions_ends_list'),
    # path('students/subscription/<int:pk>/update/', SubscriptionUpdateView.as_view(), name='subscription_edit'),
    # path('students/subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    # path('students/course/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # path('students/send-email/', views.compose_email, name='send_email'),
    #path('email-search/', EmailSearchView.as_view(), name='email_search'),
    path('students/courses/list', CourseListView.as_view(), name='course_list'),
]