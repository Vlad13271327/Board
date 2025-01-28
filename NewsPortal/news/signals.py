from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import PostCategory, Author
from .tasks import send_notifications

@receiver(post_save, sender=Author)
def send_hello_email(sender, instance, created, **kwargs):
    if created:  # только для новых авторов

        msg = EmailMultiAlternatives(
            subject='Поздравляем, теперь вы автор!',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.user.email],
        )
        msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_notifications.delay(instance.pk)

# @receiver(m2m_changed, sender=PostCategory)
# def send_notifications( sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         pk = instance.pk
#         title = instance.title
#         preview = instance.preview()
#         categories = instance.category.all()
#         subscribers_emails = []
#
#         for category in categories:
#             subscribers = category.subscribers.all()
#             subscribers_emails += [subscriber.email for subscriber in subscribers]
#
#         subscribers_emails = set(subscribers_emails)
#
#         msg = EmailMultiAlternatives(
#             subject=f'Новая статья в категории: {", ".join([category.name for category in categories])}',
#             body=f'Здравствуйте! Появилась новая статья: {title}\n'
#                  f'Краткое содержание: {preview}\n\n'
#                  f'Полный текст статьи доступен по ссылке: {settings.SITE_URL}/news/{pk}',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=subscribers_emails,
#             )
#         msg.send()