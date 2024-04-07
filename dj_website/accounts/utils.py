from django.conf import settings
from django.core.mail import send_mail
from accounts.models import User
from django.template.loader import render_to_string


def send_welcome_email(user=User, fail_silently=False):
    if user.email:
        subject = render_to_string(
            template_name="accounts/welcome_email/subject.txt",
            context={},
        )
        subject = " ".join(subject.splitlines())
        content = render_to_string(
            template_name="accounts/welcome_email/content.txt",
            context={
                "username": user.username,
            },
        )
        sender = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(
            subject,
            content,
            sender,
            recipient_list,
            fail_silently=fail_silently,
        )
