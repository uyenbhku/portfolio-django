from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import os
from dotenv import load_dotenv

load_dotenv()

admin_email = os.getenv("ADMIN_EMAIL")
service_email = os.getenv("MY_EMAIL")

def send_email(name: str, email: str, content: str, subject: str = '', cc: list = []):
    # Prepare the email content
    subject = subject if subject else f"NEW MESSAGE FROM {name}"
    body = f"Subject: {subject}\nFrom: {name} - {email}\n\n{content}"

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=subject,
            body=body,
            from_email=service_email,
            to=[email],
            cc=cc + [admin_email],
            connection=connection,
        ).send(fail_silently=True,)


def send_thankyou_email(name: str, email: str, cc: list = []):
    subject = "Thank you for contacting"

    html_message = render_to_string("emails/thank_you.html", {
        'name': name,
        'link_to_portfolio': os.getenv('LINK_TO_PORTFOLIO'), 
        'my_name': os.getenv('ADMIN_NAME')
    })
    plain_message = strip_tags(html_message)
     
    with mail.get_connection() as connection:
        email = mail.EmailMessage(
            subject=subject,
            body=html_message,
            from_email=service_email,
            to=[email],
            cc=[admin_email],
            reply_to=[admin_email],
            connection=connection,
        )
        email.content_subtype='html'
        email.send(fail_silently=True,)