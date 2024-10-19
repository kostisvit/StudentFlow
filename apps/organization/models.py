from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

class Organization(TimeStampedModel):
    owner_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    is_active = models.BooleanField(default=True)
    
    
    class Meta:
        ordering = ['title']
        verbose_name = _('Οργανισμός')
        verbose_name_plural = _('Οργανισμός')
    
    def __str__(self):
        return f"{self.title}"

