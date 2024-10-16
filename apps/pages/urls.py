from django.urls import path
from . import views
from .views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('app/updates', views.update_info_view, name='update_list'),
    
]