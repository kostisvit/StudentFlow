from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class UpdateInfo(TimeStampedModel):
    update_version = models.ForeignKey('UpdateVersion', related_name='versions', on_delete=models.CASCADE)
    update_info = models.CharField(max_length=250, blank=True, null=True)
  
    class Meta:
        verbose_name = _('Αναβαθμίσεις')
        verbose_name_plural = _('Αναβαθμίσεις')
  
    def __str__(self):
      return self.update_info if self.update_info else ""

class UpdateVersion(TimeStampedModel):
    version = models.CharField(max_length=50, blank=True, null=True)
  
    class Meta:
        verbose_name = _('Έκδοση Εφαρμογής')
        verbose_name_plural = _('Έκδοση Εφαρμογής')
  
    def __str__(self):
      return self.version
    
