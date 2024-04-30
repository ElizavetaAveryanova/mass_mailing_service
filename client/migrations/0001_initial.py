# Generated by Django 5.0.4 on 2024-04-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='фамилия')),
                ('first_name', models.CharField(max_length=50, verbose_name='имя')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='отчество')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('comment', models.CharField(max_length=250, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
    ]
