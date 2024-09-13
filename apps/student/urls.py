# urls.py
from django.urls import path
from .views import StudentListView
#SubscriptionListView,SubscriptionCreateView,Export_data_subscription,courceview,delete_entry, SubscriptionUpdateView,SubscriptionDeleteView,compose_email,SubscriptionEndingListView
from . import views

urlpatterns = [
    path('students/list', StudentListView.as_view(), name='students_list'),
    # path('students/subscriptions/', SubscriptionListView.as_view(), name='subscriptions_list'),
    # path('students/subscriptions/export', views.Export_data_subscription, name='subscriptions_list_export'),
    # path('students/subscription/new', SubscriptionCreateView.as_view(), name='subscriptions_new'),
    # path('students/subscriptions/ending', SubscriptionEndingListView.as_view(), name='subscriptions_ending_list'),
    # path('students/subscription/<int:pk>/update/', SubscriptionUpdateView.as_view(), name='subscription_edit'),
    # path('students/subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    # path('students/course/new', views.courceview, name='course_list_new'),
    # path('students/course/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # path('students/send-email/', views.compose_email, name='send_email'),
    #path('email-search/', EmailSearchView.as_view(), name='email_search'),
]