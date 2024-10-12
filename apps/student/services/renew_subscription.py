


from datetime import timedelta
from django.utils import timezone


def renew_subscription(subscription):
    from ..models import Subscription
    """
    Creates a new subscription row for the user if the current subscription is paid.
    """
    # Ensure that the subscription is paid before renewing
    if subscription.is_paid:
        # Create a new subscription entry with updated dates
        new_subscription = Subscription(
            user=subscription.user,
            student=subscription.student,
            course=subscription.course,
            is_online=subscription.is_online,
            start_date=subscription.end_date + timedelta(days=1),  # New subscription starts the day after the current end_date
            days=subscription.days,
            end_date=subscription.end_date + timedelta(days=subscription.days),
            is_paid=subscription.is_paid  # Carry over the payment status
        )
        new_subscription.save()  # Save the new subscription
        return new_subscription
    return None
