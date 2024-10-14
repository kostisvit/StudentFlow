from django.shortcuts import render, redirect
from .models import Organization
from .forms import OrganizationForm
from users.models import User


def organization_detail(request):
    if request.user.is_superuser:
        # If the user is a superuser, show all organizations
        organizations = Organization.objects.all()
    else:
        # Otherwise, show only the organization of the logged-in user
        user_organization = request.user.organization
        organizations = Organization.objects.filter(id=user_organization.id) if user_organization else []

    # Pass the organizations to the template
    context = {
        'organizations': organizations
    }
    
    return render(request, 'app/organization/organization_info.html', context)
