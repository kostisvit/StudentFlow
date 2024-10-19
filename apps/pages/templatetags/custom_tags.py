from django import template
from pages.models import UpdateVersion  # Make sure to adjust the import according to your model structure

register = template.Library()

@register.simple_tag
def get_latest_update_version():
    """
    Returns the latest UpdateVersion based on the created date or primary key.
    """
    try:
        # Fetch the latest UpdateVersion, assuming you have a `created` field or can use `id`.
        return UpdateVersion.objects.latest('created')  # If using `created` field
        # return UpdateVersion.objects.latest('id')  # If no `created` field, use id for latest
    except UpdateVersion.DoesNotExist:
        return None  # In case no versions are available