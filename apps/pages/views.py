from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin,TemplateView):
  template_name = 'home.html'
  

# class UpdateAppView(LoginRequiredMixin,TemplateView):
#   template_name = 'app/updates/update.html'
