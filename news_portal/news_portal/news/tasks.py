from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Post
from celery import shared_task

import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from news_portal.news_portal.settings import SITE_URL, DEFAULT_FROM_EMAIL


def send_weekly_email_notifications():
    subscribed_users = User.objects.filter(subscribed_categories__isnull=False).distinct()

    for user in subscribed_users:
        subscribed_categories = user.subscribed_categories.all()

        last_week = timezone.now() - timezone.timedelta(weeks=1)
        recent_posts = Post.objects.filter(date__gte=last_week, categories__in=subscribed_categories).distinct()

        if recent_posts:
            email_subject = "Weekly News Update"
            email_html_message = render_to_string('account/weekly_email.html',
                                                  {'posts': recent_posts, 'username': user.username})
            email_plaintext_message = strip_tags(email_html_message)

            send_mail(
                email_subject,
                email_plaintext_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=email_html_message
            )


#st--------------
@shared_task
def send_last_weekly_list():
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=7)
    last_week_posts = Post.objects.filter(time_create__gt=start_date)
    for name in Category.objects.all():
        post_list = last_week_posts.filter(categories=name)
        if post_list:
            subscribers = name.subscribers.values('email')
            recipients = []
            for subscriber in subscribers:
                recipients.append(subscriber['email'])
            html_content = render_to_string(
                'weekly_email.html',
                {
                    'link': settings.SITE_URL,
                    'posts': last_week_posts,
                }
            )

    msg = EmailMultiAlternatives(
        subject= f'LAST WEEK POSTS',
        body=' ',
        from_email=DEFAULT_FROM_EMAIL,
        to=recipients
        )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


