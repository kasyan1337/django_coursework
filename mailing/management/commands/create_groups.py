from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from mailing.models import CustomUser


class Command(BaseCommand):
    help = 'Creates user groups and assigns permissions'

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='managers')

        if created:
            user_content_type = ContentType.objects.get_for_model(CustomUser)
            permissions = [
                Permission.objects.get(codename='view_mailing'),
                Permission.objects.get(codename='view_client'),
                Permission.objects.get(codename='view_message'),
                Permission.objects.get(codename='view_customuser', content_type=user_content_type),
                Permission.objects.get(codename='change_customuser', content_type=user_content_type)
            ]
            manager_group.permissions.set(permissions)
            manager_group.save()