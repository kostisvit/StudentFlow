


from datetime import timedelta
from django.utils import timezone
from ..models import Subscription

def renew_subscription(subscription):
    """
    Creates a new subscription row for the user if the current subscription is paid.
    """
    # if not subscription.is_paid:
    #     raise ValueError("Cannot renew subscription: Payment is not completed.")
    
    # Create a new subscription entry with updated dates
    new_subscription = Subscription(
        user=subscription.user,
        student=subscription.student,
        course=subscription.course,
        is_online=subscription.is_online,
        start_date=subscription.end_date + timedelta(days=1),  # New subscription starts the day after the current end_date
        days=subscription.days,
        end_date=subscription.end_date + timedelta(days=subscription.days),
        is_paid=subscription.is_paid
        )

    
    new_subscription.save()
    return new_subscription
