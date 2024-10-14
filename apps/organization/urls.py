from django.urls import path
from .views import organization_detail

urlpatterns = [
    path('organization_info/', organization_detail, name='organization_info')
]