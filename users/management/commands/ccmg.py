from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from blog.models import Article


class Command(BaseCommand):
    """Создание группы Контент-менеджер"""
    def handle(self, *args, **options):
        group = Group(name='Контент-менеджер')
        group.save()
        article_content_type = ContentType.objects.get_for_model(Article)
        add_permission = Permission.objects.get(codename="add_article", content_type=article_content_type)
        change_permission = Permission.objects.get(codename="change_article", content_type=article_content_type)
        delete_permission = Permission.objects.get(codename="delete_article", content_type=article_content_type)
        group.permissions.add(add_permission, change_permission, delete_permission)
