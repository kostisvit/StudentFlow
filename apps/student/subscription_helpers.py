from django.utils import timezone

def is_subscription_expired(end_date):
    """
    Check if the subscription has expired by comparing the end_date with the current date.
    """
    return timezone.now().date() > end_date

def mark_subscription_expired(subscription):
    """
    Mark the given subscription as expired if it has passed the end_date.
    """
    if is_subscription_expired(subscription.end_date):
        subscription.is_online = False
        subscription.save()