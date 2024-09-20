import random
from django.urls import reverse
from django.db import models
from django.utils import timezone
from organization.models import Organization
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Student(TimeStampedModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True)
    is_student = models.BooleanField(default=False,null=True, blank=True)
    membership_number = models.CharField(max_length=10, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.membership_number:
            self.membership_number = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            membership_number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            if not Student.objects.filter(membership_number=membership_number).exists():
                break
        return membership_number
    
    def get_absolute_url_edit(self):
        return reverse("student_edit", kwargs={'pk': self.pk})
    
    def get_absolute_url_delete(self):
        return reverse("student_delete", args=[str(self.id)])
    
    
    def __str__(self):
        return f"{self.user}"


    class Meta:
        ordering = ['user']
        verbose_name = _('Student')
        verbose_name_plural = _('Student')


class Course(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True,related_name='courses')
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Subscription(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    days = models.PositiveIntegerField(default=30)
    end_date = models.DateField(editable=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user}"
    
    def get_absolute_url_edit(self):
        return reverse("subscription_edit", args=[str(self.id)])
    
    def get_absolute_url_delete(self):
        return reverse("subscription_delete", args=[str(self.id)])