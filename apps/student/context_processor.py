from .models import *
from datetime import timedelta
from django.utils import timezone
from django.db.models import F

# filter subscription by user company
def subscriptions_count(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Return all data if the user is a superuser
            data = Subscription.objects.filter(is_online=True).count()
        else:
            # Return only the user's data
            data = Subscription.objects.filter(is_online=True,student__user__organization=request.user.organization).count()
        return {
            'subscriptions_count': data
        }
    return {
        'subscriptions_count': None
    }


# subscription count
def subscriptions_expired(request):
    # Define the threshold for "closing soon" (e.g., 15 days)
    today = timezone.now().date()
    end_date_threshold = today + timedelta(days=30)

    count = Subscription.objects.filter(end_date__lte=timezone.now().date()).count()

    return {'subscriptions_expired': count}


# course count
def course_count(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            data = Course.objects.filter(is_online=True).count()
        else:
            data = Course.objects.filter(is_online=True,organization=request.user.organization).count()
        return {
            'course_count': data
        }
    return {
        'course_count': None
    }