from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import UpdateInfo

#fake view for testing
from django.http import HttpResponse
def fake_view(request):
    return HttpResponse("This is a fake view for testing purposes.")



@login_required
def homePageView(request):
    user = request.user  # get the logged-in user
    return render(request, 'home.html', {'user': user})


@login_required
def update_info_view(request):
    # Fetch all update info records
    updates = UpdateInfo.objects.select_related('update_version').all()

    # Group the updates by version
    grouped_updates = {}
    for update in updates:
        version = update.update_version
        if version not in grouped_updates:
            grouped_updates[version] = {
                'created': update.created,  # Store the created date of the first record
                'infos': []
            }
        grouped_updates[version]['infos'].append(update.update_info)
    
    return render(request, 'app/update_list.html', {'grouped_updates': grouped_updates})