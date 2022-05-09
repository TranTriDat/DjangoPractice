from __future__ import absolute_import, unicode_literals
from .models import User
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
import practice1.settings as settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import generate_token
from datetime import datetime
from django.db import connection
from practice1.celery import app

# app = celery.app
DB_HEALTH_CHECKED = "Database health checked"
DB_HEALTH_ERROR = "Database is not working!"
DB_USER_SIGNED_UP_AFTER_A_DAY = "List of users signed up for today"


def list_users(date):
    list_user_today = []
    all_users = User.objects.all()

    for user in all_users:
        date_joined = user.date_joined
        if datetime.date(date_joined) == date:
            list_user_today.append(user.username)

    return list_user_today


today = datetime.date(datetime.now())
user_date_joined = list_users(today)
print(user_date_joined)


@app.task
def send_email_task(subject, message, to_list):
    from_email = settings.EMAIL_HOST_USER
    return send_mail(subject, message, from_email, to_list, fail_silently=True)


@shared_task
def user_signed_up(request, myuser):
    # Welcome Email
    subject = "Welcome Email"
    message = "Hello " + myuser.username + "!!\n" + "Welcome\n Please confirm your email"
    from_email = settings.EMAIL_HOST_USER
    to_list = [myuser.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

    # Email Confirmation
    current_site = get_current_site(request)
    email_subject = "Confirm your email - Django Practice Login Step"
    message2 = render_to_string('email_confirmation.html', {
        'name': myuser.username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': generate_token.make_token(myuser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
    )
    email.fail_silently = True
    email.send()
    return "Send mail to " + myuser.username + "!"


@app.task
def health_check_task():
    email_subject = "Updated DB Health Check Situation"
    checking = connection.settings_dict
    if checking:
        message = DB_HEALTH_CHECKED
        return message
    else:
        message = DB_HEALTH_ERROR
        to_list = [settings.EMAIL_HOST_USER]
        return send_email_task.delay(email_subject, message, to_list)


@app.task
def list_user_signed_up_today_task():
    email_subject = DB_USER_SIGNED_UP_AFTER_A_DAY

    to_list = [settings.EMAIL_HOST_USER]
    message = "Users Signed Up:\n"
    for i in user_date_joined:
        message += "\t".join(i) + "\n"
    send_email_task.delay(email_subject, message, to_list)
    print("Sent Report to Admin about total signed up today")

# Celery worker: celery -A practice1 worker -l info -P gevent
# Celery beat: celery -A practice1 beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
