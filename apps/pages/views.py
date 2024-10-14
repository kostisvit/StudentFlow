from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

#fake view for testing
from django.http import HttpResponse
def fake_view(request):
    return HttpResponse("This is a fake view for testing purposes.")


class HomePageView(LoginRequiredMixin,TemplateView):
  template_name = 'home.html'


class UpdateListView(LoginRequiredMixin,ListView):
    model = ''
    template_name = 'app/update_list.html'
    context_object_name = 'updates'
