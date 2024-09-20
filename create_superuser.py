import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tu_proyecto.settings")  # Cambia "tu_proyecto" por el nombre de tu proyecto
django.setup()

User = get_user_model()

# Configura los valores del superusuario
per_documento = '1234567890'
per_nombres = 'Admin'
email = 'estadisticasenacomercio@gmail.com'
password = 'estadistica12345'

# Verifica si el superusuario ya existe
if not User.objects.filter(email=email).exists():
    user = User.objects.create_superuser(
        username=per_documento,  # Usa el documento como nombre de usuario
        email=email,
        password=password
    )
    user.per_nombres = per_nombres  # Asigna el nombre
    user.save()  # Guarda los cambios
    print(f'Superuser {per_documento} creado con éxito.')
else:
    print('El superusuario ya existe.')
