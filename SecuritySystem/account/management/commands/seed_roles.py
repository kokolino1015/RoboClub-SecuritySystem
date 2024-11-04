from django.core.management.base import BaseCommand
from SecuritySystem.account.models import Role

class Command(BaseCommand):
    help = "Seed initial roles: Admin, Observer, Normal User"

    def handle(self, *args, **kwargs):
        roles = [
            'admin',
            'observer',
            'normal_user',
        ]

        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role '{role}' created successfully."))
            else:
                self.stdout.write(f"Role '{role}' already exists.")
