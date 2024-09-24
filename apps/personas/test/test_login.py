from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from apps.personas.models import Persona
from django.contrib.messages import get_messages
class InicioSesionTests(TestCase):

    def setUp(self):
        
        self.user = Persona.objects.create_user(
            per_documento=987654321,
            per_tipo_documento='CC',  # Asegúrate de que este tipo de documento exista
            email='test@example.com',
            password='nova12345678',
            per_nombres='Nombre Test',
            per_apellidos='Apellido Test',
            per_telefono='1234567890'
    )
        print(f'Usuario creado: {self.user}')  # Verifica que el usuario se creó correctamente


    def test_inicio_sesion_exitoso(self):
        # Simula el inicio de sesión con credenciales correctas
        response = self.client.post(reverse('personas:inicio_sesion'), {
            'per_documento': 987654321,       # Debe coincidir con lo que usaste para crear el usuario
            'password1': 'nova12345678',       # Debe coincidir con la contraseña del usuario
        })
        self.assertRedirects(response, reverse('cores:general'))  # Verifica que se redirige correctamente
    