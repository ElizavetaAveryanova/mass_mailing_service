from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import datetime
import os
import pytz

from blog.models import Article
from mailing.models import Mailing, Log


def send_email(mailing, client):
    """Функция отправки сообщения выбранному контакту"""

    recipient_list = [client.email]
    server_response = ""
    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
    except Exception as expt:
        server_response = expt
        try_status = 'Failed'
    else:
        try_status = 'Ok'

    #  добавление записи в лог
    Log.objects.create(
        mailing=mailing,
        contacts=client,
        try_status=try_status,
        server_answer=server_response
    )

def send_email(mailing, client):
    """Функция отправки сообщения выбранному контакту"""
    recipient_list = [client.email]
    server_response = ""
    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
    except Exception as expt:
        server_response = expt
        try_status = 'Failed'
    else:
        try_status = 'Ok'

    Log.objects.create(
        mailing=mailing,
        contacts=client,
        try_status=try_status,
        server_answer=server_response
    )

def send_mails():
    """Функция запуска рассылки"""
    print('Привет')
    now = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))  # получение текущей даты и времени в UTC
    for mailing in Mailing.objects.filter(status='STARTED'):  # цикл по всем активным (со статусом 'STARTED') рассылкам
        for client in mailing.client.all():  # для клиента среди всех контактов рассылки
            log = Log.objects.filter(mailing=mailing, contacts=client).order_by('-try_time').first()  # получение последней записи лога для текущей рассылки и контакта
            if log:
                last_try_time = log.try_time.astimezone(pytz.timezone(settings.TIME_ZONE))  # получение времени последней попытки отправки в UTC
                if now < mailing.datetime_finish.astimezone(pytz.timezone(settings.TIME_ZONE)):  # не истекло ли время окончания рассылки
                    if mailing.period == 'DAILY':  # является ли рассылка ежедневной
                        if (now - last_try_time).days >= 1:  # прошло ли не менее 1 дня с момента последней попытки отправки
                            send_email(mailing, client)
                    elif mailing.period == 'WEEKLY':  # является ли рассылка еженедельной
                        if (now - last_try_time).days >= 7:
                            send_email(mailing, client)
                    elif mailing.period == 'MONTHLY':  # является ли рассылка ежемесячной
                        if (now - last_try_time).days >= 30:
                            send_email(mailing, client)
                else:
                    mailing.status = 'FINISHED'
                    mailing.save()
            else:
                if now >= mailing.datetime_start.astimezone(pytz.timezone(settings.TIME_ZONE)):
                    send_email(mailing, client)
                    if mailing.period == 'ONCE':  # является ли рассылка единоразовой
                        mailing.status = 'FINISHED'
                        mailing.save()
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
def main():
    recipient_list = os.getenv('RECIPIENT_LIST', '').split(',')
    if recipient_list:
        send_mails()
    else:
        print('RECIPIENT_LIST not set in .env file')

if __name__ == '__main__':
    main()

