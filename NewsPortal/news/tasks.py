from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

@shared_task
def send_weekly_posts():
    one_week_ago = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(date_in__gte=one_week_ago)
    categories = posts.values_list('category__name', flat=True)
    subscribers_email = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_message = render_to_string('weekly_summery.html', {'recent_posts': posts})
    text_message = strip_tags(html_message)

    send_mail(
        subject='Еженедельная рассылка новостей',
        message=text_message,  # Текстовая версия
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=subscribers_email,
        html_message=html_message,  # HTML-версия
    )

@shared_task
def send_notifications(pk):
    post = Post.objects.get(pk=pk)
    # pk = post.pk
    title = post.title
    preview = post.preview()
    categories = post.category.all()
    subscribers_emails = []

    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails += [subscriber.email for subscriber in subscribers]

    subscribers_emails = set(subscribers_emails)

    msg = EmailMultiAlternatives(
        subject=f'Новая статья в категории: {", ".join([category.name for category in categories])}',
        body=f'Здравствуйте! Появилась новая статья: {title}\n'
             f'Краткое содержание: {preview}\n\n'
             f'Полный текст статьи доступен по ссылке: {settings.SITE_URL}/news/{pk}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
        )
    msg.send()