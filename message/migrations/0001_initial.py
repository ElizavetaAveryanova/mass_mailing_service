# Generated by Django 5.0.4 on 2024-04-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, verbose_name='тема')),
                ('text', models.TextField(verbose_name='текст')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
    ]
