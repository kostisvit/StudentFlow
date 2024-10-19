from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePageView, name='home'),
    path('app/updates', views.update_info_view, name='update_list'),
    
]