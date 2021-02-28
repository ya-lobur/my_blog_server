import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from my_blog_server.celery import app
from my_blog_server import settings


@app.task
def send_verification_email(profile_id):
    ProfileModel = get_user_model()

    try:
        profile = ProfileModel.objects.get(pk=profile_id)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
            'http://localhost:8000%s' % reverse('user_profile:verify', kwargs={'uuid': str(profile.verification_uuid)}),
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
    except ProfileModel.DoesNotExist:
        logging.warning(f"Tried to send verification email to non-existing profile '{profile_id}'")
