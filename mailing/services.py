import smtplib
from django.core.mail import send_mail

from config import settings
from config.settings import EMAIL_HOST_USER
import pytz
from datetime import datetime
from django.core.cache import cache
from mailing.models import Mailing, Log
from blog.models import Article

MY_TIME_ZONE = pytz.timezone(settings.TIME_ZONE)
NOW = datetime.now(MY_TIME_ZONE)

def send_mail_func(mailing):
    """Отправляет письмо на почту клиентам из рассылки, записывает попытки рассылки"""
    client_emails = mailing.clients.values_list('email', flat=True)
    subject = mailing.message.subject
    text_of_message = mailing.message.text
    try:
        send_response = send_mail(
            subject=subject,
            message=text_of_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=client_emails,
            fail_silently=False,
        )
        # Log.objects.create(try_time=NOW, try_status=Log.SUCCESS, server_answer=send_response,
        #                       mailing=mailing, clients=client)
        for client in mailing.clients.all():
            Log.objects.create(try_time=NOW, try_status=Log.SUCCESS, server_answer=send_response,
                               mailing=mailing, clients=client)
        return send_response
    except smtplib.SMTPException as e:
        Log.objects.create(try_time=NOW, try_status=Log.FAIL, server_answer=e,
                              mailing=mailing, clients=client)


def send_mails():
    """Запускает рассылки, меняет их статусы, проверяет периодичность"""
    mailings = (Mailing.objects.filter(status__in=['created', 'started']).filter(datetime_start__lte=NOW).
                prefetch_related('clients').select_related('message'))

    for mailing in mailings:
        print('прошел по рассылке')

        if mailing.datetime_finish < NOW:
            mailing.status = Mailing.FINISHED
            mailing.save()
            print('отработал статус FINISHED')

        elif mailing.status == Mailing.CREATED:
            send_mail_func(mailing)
            mailing.status = Mailing.STARTED
            mailing.save()
            print('Отработала отправка и смена статуса на STARTED')

        elif mailing.status == Mailing.STARTED:
            try_time = Log.objects.filter(mailing=mailing).order_by('try_time').first()
            if try_time:
                delta = NOW - try_time.try_time
                if mailing.period == Mailing.DAILY and delta.days >= 1:
                    send_mail_func(mailing)
                elif mailing.period == Mailing.WEEKLY and delta.days >= 7:
                    send_mail_func(mailing)
                elif mailing.period == Mailing.MONTHLY and delta.days >= 30:
                    send_mail_func(mailing)
                print('Отработала отправка рассылки со статусом Запущена')

    print(f'Текущее время:{NOW}')

def get_cashed_article_list():
    """Функция возвращает закешированный список статей"""

    key = 'articles'
    article_list = Article.objects.all()

    if settings.CACHE_ENABLED:
        articles = cache.get(key)
        if articles is None:
            articles = article_list
            cache.set(key, articles)
        return articles

    return article_list
