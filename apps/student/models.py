import random
from django.urls import reverse
from django.db import models
from django.utils import timezone
from organization.models import Organization
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

class Student(TimeStampedModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True)
    course = models.ForeignKey("student.Course", on_delete=models.CASCADE,null=True, blank=True)
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
        return reverse("student_edit", args=[str(self.id)])
    
    def get_absolute_url_delete(self):
        return reverse("student_delete", args=[str(self.id)])
    
    
    def __str__(self):
        return f"{self.user}"


    class Meta:
        ordering = ['user']
        verbose_name = _('Μαθητές')
        verbose_name_plural = _('Μαθητές')


class Course(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True,related_name='courses')
    user = models.ForeignKey("users.User", on_delete=models.CASCADE,default='1',null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.user}" if self.user else f"{self.title}"

    class Meta:
        ordering = ['title']
        verbose_name = _('Μαθήματα')
        verbose_name_plural = _('Μαθήματα')



class Enrollment(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    is_online = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


from .subscription_helpers import is_subscription_expired

class Subscription(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    days = models.PositiveIntegerField(default=30)
    end_date = models.DateField(editable=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']
        verbose_name = _('Εγγραφές')
        verbose_name_plural = _('Εγγραφές')

    def __str__(self):
        return f"{self.student.user}"

    def save(self, *args, **kwargs):
            # On creation, set the end_date to 'start_date + duration' days
            if not self.end_date:
                self.end_date = self.start_date + timedelta(days=self.days)
            super().save(*args, **kwargs)

    def is_expired(self):
            # Use the helper function to check if the subscription is expired
        return is_subscription_expired(self.end_date)

    # def mark_expired(self):
    #         # Use the helper function to mark the subscription as expired
    #     mark_subscription_expired(self)

    def __str__(self):
        return f"Subscription: {self.start_date} to {self.end_date}, Status: {self.is_online}"


    # @property
    # def days_active(self):
    #     delta = self.end_date - self.start_date
    #     return delta.days

    # @property
    # def is_short_term(self):
    #     # Returns True if the subscription is 15 days or shorter
    #     return self.days_active <=15

    # # A flag to prevent recursion
    # _is_creating_new_subscription = False

    def save(self, *args, **kwargs):
        # If it's a new subscription or the end_date is not set, calculate the end date
        if not self.end_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.days)

        # Save the current subscription without creating any new ones
        super(Subscription, self).save(*args, **kwargs)
    
    def get_absolute_url_delete(self):
        return reverse("subscription_delete", args=[str(self.id)])