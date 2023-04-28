from django_project.celery import app
from django.core.mail import send_mail

#for email
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage


@app.task
def send_reset_mail(subject_template_name, email_template_name, from_email, to_email, html_email_template_name, context):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """

    # send_mail(
    #     'sdfsdfadsfsdfsadf', ['nnnooo2@yandex.ru'], fail_silently=False,
    # )

    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    #
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
    email_message.send()

@app.task
def send_code_mail(email, code):
    """
    Send a mail`.
    """

    # send_mail(
    #     'sdfsdfadsfsdfsadf', ['nnnooo2@yandex.ru'], fail_silently=False,
    # )

    mail_subject = 'Activation code has been sent to your email'
    message = 'Ваш код октивации: ' + str(code)
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
