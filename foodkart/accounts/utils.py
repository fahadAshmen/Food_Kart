from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from . models import Account
from django.core.exceptions import PermissionDenied


def send_notification(mail_subject,mail_template,context):     
    from_mail = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template,context)
    to_email= context['vendor'].email
    print(to_email)
    send_email = EmailMessage(mail_subject, message, from_mail, to=[to_email])
    send_email.send()

def check_role_vendor(user):
    if user.role == 'VENDOR':
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 'CUSTOMER':
        return True
    else:
        raise PermissionDenied



