from django.test import TestCase
from django.urls import reverse
import pandas as pd
import io
from django.contrib.auth.models import Permission
from datetime import date
from unittest.mock import patch
from apps.personas.models import Persona,Persona_rol,Rol
from django.contrib.auth import get_user_model
import uuid
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta
class SubirPoblacionVulnerableTestCase(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        # Crea un rol con permisos
        cls.role = Rol.objects.create(
            rol_nombre='Admin',
            rol_descripcion='Administrador del sistema'
        )
        # Asigna el permiso al rol
        content_type = ContentType.objects.get_for_model(Persona)
        permission = Permission.objects.create(
            codename='can_view_reporteador_dashboard',
            name='Can view reporteador dashboard',
            content_type=content_type
        )
        cls.role.permissions.add(permission)

        # Crea un usuario de prueba y asigna el rol
        cls.user = Persona.objects.create_user(
            per_documento=1234567890,
            email='dayana@example.com',
            password='testpassword12345'
        )
        
        Persona_rol.objects.create(
            persona_id=cls.user,
            rol_id=cls.role,
            rolp_fecha_inicio=date.today(),
            rolp_fecha_fin=date.today(),  # Ajusta la fecha según tus requisitos
            rolp_estado=True
        )
        cls.fecha_inicio = datetime(2020, 1, 1)
        cls.fecha_fin = datetime(2025, 12, 31)
        
        cls.excel_data = {
            'Grupos': ['Grupo A', 'Grupo B'],
            'Porcentaje_ejecicion': [50, 70],
            'Indicadores_poblaciones': ['Indicador 1', 'Indicador 2'],
            'Grupos_poblaciones': ['Grupo 1', 'Grupo 2'],
            'Meta_2024_poblaciones': [100, 200],
            'Ejecucion_poblaciones': [30, 50],
            'porcentaje_de_poblaciones': [30, 25],
        }
        
        # Convertir los datos en un DataFrame y luego a un archivo Excel en memoria
        cls.df = pd.DataFrame(cls.excel_data)
        cls.excel_file = io.BytesIO()
        with pd.ExcelWriter(cls.excel_file, engine='xlsxwriter') as writer:
            cls.df.to_excel(writer, sheet_name='RESUMEN', index=False)

        cls.excel_file.seek(0) 
     

    def test_permission_required(self):
        """Prueba que la vista P04 requiere permisos."""
        url = reverse('personas:P04')

        # Verifica que un usuario sin autenticación obtenga un 403
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Autentica al usuario
        self.client.force_login(self.user)

        # Verifica si el usuario tiene el permiso
        has_permission = self.user.has_perm('personas.can_view_reporteador_dashboard')
        print(f"Permiso 'can_view_reporteador_dashboard' para el usuario: {'Sí' if has_permission else 'No'}")
        
        # Intenta acceder a la vista con el usuario autenticado
        response = self.client.get(url)

        # Verifica que el usuario autenticado con permiso obtenga acceso
        self.assertEqual(response.status_code, 200)  # Reiniciar el puntero del archivo a la posición inicial

    @patch('apps.personas.views.Persona.objects.get')  # Simular la consulta a Persona
    def test_subir_poblacion_vulnerable_success(self, mock_get):
        # Simular un objeto Persona devuelto por el mock
        
        self.client.force_login(self.user)
        mock_get.return_value = self.user.per_documento   # Retornar el objeto Persona creado

        # Realizar la solicitud POST
        response = self.client.post(reverse('personas:upload_excel'), {
            'excel_file': self.excel_file,
            'per_documento': self.user.per_documento  # Usar el documento del usuario
        })

        # Verificar la respuesta
        self.assertEqual(response.status_code, 302)  # Verificar redirección (código 302)

    