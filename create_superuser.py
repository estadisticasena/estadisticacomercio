from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser with specified credentials'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        per_nombres = 'admin' 
        per_documento=1234567890
        email = 'estadisticasenacomercio@gmail.com'
        password = 'estadistica12345'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        else:
            User.objects.create_superuser(
                per_nombres=per_nombres,
                per_documento=per_documento,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {per_nombres} created successfully.'))

