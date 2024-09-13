from django.shortcuts import render, redirect
from .models import Organization
from .forms import OrganizationForm


def organization_detail(request):
    # Get the company associated with the logged-in user
    organization = Organization.objects.filter(customuser=request.user).first()

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to a view that shows company details or a success page
    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'app/organization/organization_info.html', {'organizationform': form})
