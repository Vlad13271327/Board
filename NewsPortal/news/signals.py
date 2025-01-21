from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from .models import PostCategory


@receiver(post_save, sender=User)
def send_hello_email(sender, instance, created, **kwargs):
    if created:  # только для новых пользователей
        html_content = render_to_string(
            'email/new_author.html',
            {
                'user': instance,
                'site_url': settings.SITE_URL,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Добро пожаловать на наш новостной портал!',
            body=f'Здравствуйте, {instance.username}! Спасибо за регистрацию на нашем сайте.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def send_notifications(preview, pk, title, subscribers, **kwargs):
    html_content = render_to_string(
        'email/post_created.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }

    )

    msg = EmailMultiAlternatives(
        subject= title,
        body='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to = subscribers
        )


    msg.attach_alternative(html_content, 'text/html')
    msg.send()