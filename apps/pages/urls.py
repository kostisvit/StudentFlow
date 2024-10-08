from django.urls import path
from . import views
from .views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('app/updates', views.fake_view, name='update_list'),
    #path('members/updates', UpdateAppView.as_view(), name='update_app')
    
]