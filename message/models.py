from django.db import models


class Message(models.Model):
    """Сообщение для рассылки"""
    subject = models.CharField(max_length=100, verbose_name='тема')
    text = models.TextField(verbose_name='текст')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
