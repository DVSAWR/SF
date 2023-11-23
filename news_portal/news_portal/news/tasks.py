from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Post


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