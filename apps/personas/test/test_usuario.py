from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.personas.models import Persona, Rol, Persona_rol
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from datetime import date

class AsignacionRolesTests(TestCase):
    def setUp(self):
        # Crear un rol y asignar un permiso a ese rol
        self.role = Rol.objects.create(
            rol_nombre='Admin',
            rol_descripcion='Administrador del sistema'
        )

        content_type = ContentType.objects.get_for_model(Persona)
        permission = Permission.objects.create(
            codename='can_view_admin_dashboard',
            name='Can view admin dashboard',
            content_type=content_type
        )
        self.role.permissions.add(permission)

        # Crear un usuario de prueba
        self.user = Persona.objects.create_user(
            per_documento='1234567890',
            email='dayana@example.com',
            password='testpassword12345'
        )

        # Asignar el rol al usuario de prueba
        Persona_rol.objects.create(
            persona_id=self.user,
            rol_id=self.role,
            rolp_fecha_inicio=date.today(),
            rolp_fecha_fin=date.today(),  # Ajusta la fecha según tus requisitos
            rolp_estado=True
        )

        # Hacer login con el usuario de prueba
        self.client.login(email='dayana@example.com', password='testpassword12345')

        # Crear una instancia de Persona y Rol para las pruebas
        self.persona = Persona.objects.create(
            per_documento='123456789',
            email='persona@example.com',  # Agrega otros campos necesarios
            password='password123'  # Asegúrate de tener todos los campos necesarios
        )
        self.rol = Rol.objects.create(
            rol_nombre='Rol de prueba',
            rol_descripcion='Descripción del rol de prueba',
        )

    def test_asignacion_roles(self):
       

        # Autentica al usuario
        self.client.force_login(self.user)
        # Simula una solicitud POST para asignar un nuevo rol a una persona existente
        response = self.client.post(reverse('cores:asignacion_roles'), {
            'persona_id': self.persona.per_documento,
            'rol_id': self.rol.rol_id,
        })

        # Verificar que se redirige a la vista de administrador
        self.assertRedirects(response, reverse('administrador'))

        # Verificar que la persona tiene el nuevo rol asignado
        self.assertTrue(Persona_rol.objects.filter(persona_id=self.persona, rol_id=self.rol).exists())

    def test_asignacion_roles_persona_no_existe(self):
        self.client.force_login(self.user)
        # Simula una solicitud POST con un persona_id que no existe
        response = self.client.post(reverse('cores:asignacion_roles'), {
            'persona_id': '999999999',  # ID que no existe
            'rol_id': self.rol.rol_id,
        })

        # Verificar que se lanza un error 404
        self.assertEqual(response.status_code, 404)

    def test_asignacion_roles_rol_no_existe(self):
        self.client.force_login(self.user)
        
        # Obtén un ID que no exista en la base de datos
        rol_id_inexistente = 999999  # Un ID que seguramente no existe
    
        # Simula una solicitud POST con un rol_id que no existe
        response = self.client.post(reverse('cores:asignacion_roles'), {
            'persona_id': self.persona.per_documento,
            'rol_id': rol_id_inexistente,  # ID de rol que no existe
        })
    
        # Verificar que se lanza un error 404
        self.assertEqual(response.status_code, 404)


    def test_asignacion_roles_sin_post(self):
        self.client.force_login(self.user)
        # Simula una solicitud GET a la vista
        response = self.client.get(reverse('cores:asignacion_roles'))

        # Verificar que se redirige a la vista de administrador
        self.assertRedirects(response, reverse('administrador'))
