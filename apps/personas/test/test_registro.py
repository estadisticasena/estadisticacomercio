from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.personas.models import Persona, Rol, Persona_rol

class RegistroViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crea un usuario administrador de prueba
        cls.admin_user = Persona.objects.create_superuser(
            per_documento=111,
            email='admin@example.com',
            password='adminpassword'
        )

        # Crea el contenido y permiso para la vista de admin
        content_type = ContentType.objects.get_for_model(Persona)
        cls.admin_permission, created = Permission.objects.get_or_create(
            codename='can_view_admin_dashboard',
            name='Can view admin dashboard',
            content_type=content_type
        )
        cls.admin_user.user_permissions.add(cls.admin_permission)

    def test_permission_required(self):
        """Prueba que la vista Registro requiere permisos."""
        url = reverse('personas:registro')

        # Verifica que un usuario sin autenticación obtenga un 403
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Verifica que un usuario administrador con permisos puede acceder a la vista
        self.client.force_login(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_registration_creates_user_with_permissions(self):
        """Prueba que se crea un nuevo usuario con permisos de usuario."""
        self.client.force_login(self.admin_user)
    
        # Simula el registro de un nuevo usuario
        response = self.client.post(reverse('personas:registro'), {
            'per_documento': 222,  # Debe ser único
            'per_tipo_documento': 'CC',  # O el valor correcto según tus opciones
            'email': 'user@example.com',
            'per_nombres': 'John',  # Agrega este campo
            'per_apellidos': 'Doe',  # Agrega este campo
            'per_telefono': '1234567890',  # Agrega este campo
            'password1': 'userpassword',
            'password2': 'userpassword',
        })
    
        # Imprime el contenido de la respuesta para diagnóstico
        print(response.content)
    
        # Verifica que el registro redirija correctamente
        self.assertRedirects(response, reverse('administrador'))
