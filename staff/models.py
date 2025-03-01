from django.contrib.auth.models import AbstractUser
from django.db import models
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# Custom Staff model that extends AbstractUser
class Manager(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("password-reset/")+str(token)

    print(token)
    print(full_link)

    context = {
        'full_link':full_link,
        'email_address': reset_password_token.user.email
    }

    html_message = render_to_string("backend/email.html", context=context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject = "Request for resetting password for {title}".format(title=reset_password_token.user.username),
        body=plain_message,
        from_email="sender@example.com",
        to=[reset_password_token.user.email]
    )


    msg.attach_alternative(html_message, "text/html")
    msg.send()