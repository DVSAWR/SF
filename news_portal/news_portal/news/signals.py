from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string

from .models import PostCategory, Post
from django.conf import settings


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers_email = []

        for i in categories:
            subscribers = i.subscribers.all()
            subscribers_email += [s.email for s in subscribers]
        send_notifications(instance.preview, instance.pk, instance.title, subscribers_email)


def send_notifications(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'email_template.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

