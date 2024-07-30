
from .tokens import account_activation_token


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages

def activate_email(request, user, receiver):
    email_subject = 'Activate your account'
    message = render_to_string('email_templates/reset_password_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uuidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })

    email = EmailMessage(
        subject=email_subject,
        body=message,
        to=[receiver]
    )

    try:
        email.send()
        messages.success(request, f'A verification link has been sent to your email address. ({receiver}) Please check your inbox or spam folder.')
    except Exception as e:
        messages.error(request, f'Oops! It seems there was a problem while trying to send your email ({receiver}). Please try again later or contact support for assistance.')
