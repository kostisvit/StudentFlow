from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler403
from django.shortcuts import render

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)

handler403 = custom_403_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('pages.urls')),
    path('', include('organization.urls')),
    path('', include('student.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
