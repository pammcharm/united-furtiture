from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.accounts.models import AdminPasswordResetRequired


class Command(BaseCommand):
    help = "Create the default demo admin account if it does not exist."

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("admin")
            user.save(update_fields=["password"])
            AdminPasswordResetRequired.objects.update_or_create(user=user, defaults={"required": True})
            self.stdout.write(self.style.SUCCESS("Created default admin user: admin / admin"))
            return

        changed = False
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            changed = True
        if changed:
            user.save(update_fields=["is_staff", "is_superuser"])

        self.stdout.write("Default admin user already exists.")
