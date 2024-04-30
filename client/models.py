from django.db import models

NULLABLE = {'blank': True, 'null':True}

class Client(models.Model):
    """Клиент сервиса"""
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    first_name = models.CharField(max_length=50, verbose_name='имя')
    middle_name = models.CharField(max_length=50, **NULLABLE, verbose_name='отчество')
    email = models.EmailField(verbose_name='email')
    comment = models.CharField(max_length=250, verbose_name='комментарий')

    def __str__(self):
        return f'{self.last_name} {self.first_name}: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
