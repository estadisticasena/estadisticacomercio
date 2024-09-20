from django.contrib.auth import get_user_model
import os

User = get_user_model()

User.objects.create_superuser(
    username=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
    email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
    password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password123')
)
