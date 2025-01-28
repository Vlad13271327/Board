import logging

from django.conf import settings
from news.models import Post, Category
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            send_weekly_posts,
            trigger=CronTrigger(day_of_week='mon', hour='08', minute='00'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="send_weekly_posts",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_posts'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")