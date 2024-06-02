from django.db import models

from client.models import Client
from message.models import Message


class Mailing(models.Model):
    """Рассылка"""

    #  варианты периодичности рассылки
    ONCE = 'Единоразовая'
    DAILY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'

    PERIOD_CHOICES = (
        ('ONCE', 'Единоразовая'),
        ('DAILY', 'Раз в день'),
        ('WEEKLY', 'Раз в неделю'),
        ('MONTHLY', 'Раз в месяц'),
    )

    #  варианты статуса рассылки
    CREATED = 'created'
    STARTED = 'started'
    FINISHED = 'finished'

    STATUS_CHOICES = (
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    )

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение') #message
    clients = models.ManyToManyField(Client, verbose_name='контакты клиентов') #to_client
    datetime_start = models.DateTimeField(verbose_name='время начала рассылки') #first_mailing
    datetime_finish = models.DateTimeField(verbose_name='время окончания рассылки') # last_mailing
    period = models.CharField(max_length=25, choices=PERIOD_CHOICES, default='DAILY', verbose_name='периодичность') # periodicity
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='CREATED', verbose_name='статус рассылки') # status
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='автор')

    def __str__(self):
        return f'{self.datetime_start}-{self.datetime_finish}, {self.period}, {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    """Логи рассылки"""
    SUCCESS = 'success'
    FAIL = 'fail'

    STATUSES = (
        (SUCCESS, 'успешно'),
        (FAIL, 'не успешно')
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка') #newsletter
    clients = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='контакты клиентов')
    try_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки') #last_try
    try_status = models.CharField(max_length=50, choices=STATUSES, verbose_name='статус попытки') #status
    server_answer = models.CharField(max_length=250, null=True, blank=True, verbose_name='ответ почтового сервера') # server_respond

    def __str__(self):
        return f'{self.try_time}: {self.try_status}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'