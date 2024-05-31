from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import datetime

from blog.models import Article
from mailing.models import Mailing, Log


def send_email(mailing, clients):
    """Функция отправки сообщения выбранному контакту"""
    client_list = [clients.email]
    server_response = ""
    try:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client_list],
            fail_silently=False
        )
    except Exception as expt:  # обработка и сохранение сообщения об ошибке
        server_response = expt
        try_status = 'Failed'
    else:
        try_status = 'Ok'
    #  добавление записи в лог
    Log.objects.create(mailing=mailing, contacts=clients, try_status=try_status, server_answer=server_response)


def send_mails():
    """Функция запуска рассылки"""
    now = datetime.datetime.now()

    for mailing in Mailing.objects.filter(status='STARTED'):  # для рассылки среди всех запущенных рассылок
        for client in mailing.client.all():  # для контакта среди всех контактов рассылки

            log = Log.objects.filter(mailing=mailing, contacts=client)  # фильтр лога по конкретной рассылке
            if log.exists():  # если у рассылки уже ранее была попытка отправки
                last_try_time = log.order_by('-try_time').first().try_time  # время последней попытки
                if now < mailing.datetime_finish:  # если время окончания рассылки не наступило
                    # отправка сообщения в зависимости от указанной в рассылке периодичности
                    if mailing.period == 'DAILY':  # раз в день
                        if (now - last_try_time).days >= 1:
                            send_email(mailing, client)
                    elif mailing.period == 'WEEKLY':  # раз в неделю
                        if (now - last_try_time).days >= 7:
                            send_email(mailing, client)
                    elif mailing.period_id == 'MONTHLY':  # раз в месяц
                        if (now - last_try_time).days >= 30:
                            send_email(mailing, client)

                else:
                    mailing.status = 'FINISHED'  # изменение статуса рассылки на "завершена"
                    mailing.save()

            else:
                if now >= mailing.datetime_start:
                    send_email(mailing, client)
                    if mailing.period == 'ONCE':  # единоразовая
                        mailing.status = 'FINISHED'  # изменение статуса рассылки на "завершена"
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