from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Updates all superusers to have the admin user type'

    def handle(self, *args, **options):
        updated_count = CustomUser.objects.filter(is_superuser=True).update(user_type='admin')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} superuser(s) to admin user type.'))