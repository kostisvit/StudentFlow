from django.shortcuts import render, redirect
from .models import Organization
from .forms import OrganizationForm


def organization_detail(request):
    organization = Organization.objects.filter(customuser=request.user).first()

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'app/organization/organization_info.html', {'organizationform': form})
