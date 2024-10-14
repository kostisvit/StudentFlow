# email_app/views.py

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views import View
from .send_email_form import EmailForm
#from .models import CustomUser
from django.http import JsonResponse

import logging
from django.core.mail import EmailMessage
from django.conf import settings
from .send_email_form import EmailForm
from django.http import HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def compose_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            bcc = [email.strip() for email in form.cleaned_data['bcc'].split(',') if email.strip()]
            cc = [email.strip() for email in form.cleaned_data['cc'].split(',') if email.strip()]
            # Create an EmailMessage object to handle attachments
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL,[email], bcc=bcc,cc=cc)
            # Attach files to the email
            for attachment in request.FILES.getlist('attachments'):
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            try:
            # Send the email
                email.send()
            # Handle success or error here
                return render(request, 'app/send_email/send_email.html')
            except Exception as e:
                logger.error(f'Email could not be sent. Error: {str(e)}')
                return HttpResponse(f'Email could not be sent. Error: {str(e)}')
    else:
        # if request.user.is_authenticated:
        #     email = request.user.email
        #     form = EmailForm(initial={'email': email})
        # else:
            form = EmailForm()
    return render(request, 'app/send_email/send_email.html', {'form': form})
