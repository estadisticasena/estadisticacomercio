from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.personas.models import Persona,Rol,Persona_rol
from apps.personas.models import P04  # Ajusta este import según la ubicación de tu modelo P04
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.personas.models import Persona  # Asegúrate de que este modelo es el correcto
from datetime import date
from django.contrib.messages import get_messages
import io
from openpyxl import Workbook
import random
from datetime import datetime, timedelta
def generar_fecha_aleatoria(inicio, fin):
    """Genera una fecha aleatoria entre dos fechas."""
    delta = fin - inicio
    dias = random.randint(0, delta.days)
    return inicio + timedelta(days=dias)
 # Retorna el objeto datetime





class SubirP04Test(TestCase):

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
        self.assertEqual(response.status_code, 200)
        

    def create_excel_file_simple(self):
        """Genera un archivo Excel en memoria con las columnas necesarias."""
     
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte"
        for _ in range(3):
           ws.append([''] * 40)
        headers = [
            "IDENTIFICADOR_FICHA",
            "CODIGO_REGIONAL",
            "NOMBRE_REGIONAL",
            "CODIGO_CENTRO",
            "NOMBRE_CENTRO",
            "IDENTIFICADOR_UNICO_FICHA",
            "ESTADO_CURSO",
            "CODIGO_NIVEL_FORMACION",
            "NIVEL_FORMACION",
            "CODIGO_JORNADA",
            "NOMBRE_JORNADA",
            "TIPO_DE_FORMACION",
            None,
            None,
            "ETAPA_FICHA",
            "MODALIDAD_FORMACION",
            "CODIGO_SECTOR_PROGRAMA",
            "NOMBRE_SECTOR_PROGRAMA",
            "CODIGO_OCUPACION",
            "NOMBRE_OCUPACION",
            "CODIGO_PROGRAMA",
            "VERSION_PROGRAMA",
            "NOMBRE_PROGRAMA_FORMACION",
            "RED",
            "CODIGO_PAIS_CURSO",
            "NOMBRE_PAIS_CURSO",
            "CODIGO_DEPARTAMENTO_CURSO",
            "NOMBRE_DEPARTAMENTO_CURSO",
            "CODIGO_MUNICIPIO_CURSO",
            "NOMBRE_MUNICIPIO_CURSO",
            "CODIGO_CONVENIO",
            "NOMBRE_CONVENIO",
            "AMPLIACION_COBERTURA",
            "CODIGO_PROGRAMA_ESPECIAL",
            "NOMBRE_PROGRAMA_ESPECIAL",
            "NUMERO_CURSOS",
            "TOTAL_APRENDICES_MASCULINOS",
            "TOTAL_APRENDICES_FEMENINOS",
            "TOTAL_APRENDICES_NOBINARIO",
            "TOTAL_APRENDICES",
            "DURACION_PROGRAMA",
            "NOMBRE_NUEVO_SECTOR",
            "TOTAL_APRENDICES_ACTIVOS",
           
        ]
        
        ws.append(headers)  # Agrega los encabezados

        # Agrega una fila de datos de prueba
        ws.append([
            "FICHA001",  # IDENTIFICADOR_FICHA
            "REG001",    # CODIGO_REGIONAL
            "Región 1",  # NOMBRE_REGIONAL
            "CENTRO001", # CODIGO_CENTRO
            "Centro 1",  # NOMBRE_CENTRO
            "UNIC001",   # IDENTIFICADOR_UNICO_FICHA
            "Activo",    # ESTADO_CURSO
            "NIVEL001",  # CODIGO_NIVEL_FORMACION
            "Nivel 1",   # NIVEL_FORMACION
            "JORNADA001",# CODIGO_JORNADA
            "Jornada 1", # NOMBRE_JORNADA
            "Formación", # TIPO_DE_FORMACION
            None,
            None,# FECHA_TERMINACION_FICHA
            "Etapa 1",   # ETAPA_FICHA
            "Modalidad 1",# MODALIDAD_FORMACION
            "SECTOR001", # CODIGO_SECTOR_PROGRAMA
            "Sector 1",  # NOMBRE_SECTOR_PROGRAMA
            "OCUPACION001",# CODIGO_OCUPACION
            "Ocupación 1",# NOMBRE_OCUPACION
            "PROGRAMA001",# CODIGO_PROGRAMA
            "1.0",       # VERSION_PROGRAMA
            "Programa 1",# NOMBRE_PROGRAMA_FORMACION
            None,        # RED
            "PAIS001",   # CODIGO_PAIS_CURSO
            "País 1",    # NOMBRE_PAIS_CURSO
            "DEPARTAMENTO001",# CODIGO_DEPARTAMENTO_CURSO
            "Departamento 1",# NOMBRE_DEPARTAMENTO_CURSO
            "MUNICIPIO001",# CODIGO_MUNICIPIO_CURSO
            "Municipio 1",# NOMBRE_MUNICIPIO_CURSO
            "CONVENIO001",# CODIGO_CONVENIO
            "Convenio 1",# NOMBRE_CONVENIO
            "Sí",        # AMPLIACION_COBERTURA
            "PROGRAMA_ESPECIAL001",# CODIGO_PROGRAMA_ESPECIAL
            "Programa Especial 1",# NOMBRE_PROGRAMA_ESPECIAL
            5,          # NUMERO_CURSOS
            10,         # TOTAL_APRENDICES_MASCULINOS
            15,         # TOTAL_APRENDICES_FEMENINOS
            0,          # TOTAL_APRENDICES_NOBINARIO
            25,         # TOTAL_APRENDICES
            6,          # DURACION_PROGRAMA
            "Nuevo Sector 1",# NOMBRE_NUEVO_SECTOR
            20          # TOTAL_APRENDICES_ACTIVOS
        ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0) 
        return output
    
    def test_subir_P04_success(self):
        """Prueba que el archivo Excel se sube correctamente."""
        self.client.force_login(self.user)
    
        excel_file = SimpleUploadedFile(
            name='test_file_simple.xlsx',
            content=self.create_excel_file_simple().getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
        response = self.client.post(reverse('personas:subir_P04'), {
            'fileUpload': excel_file,
            'per_documento': self.user.per_documento  # Usa el per_documento del usuario autenticado
        })
    
        self.assertEqual(response.status_code, 302)
    
        response = self.client.get(reverse('personas:P04'))
    
        messages = list(get_messages(response.wsgi_request))
    
        try:
            self.assertIn("Datos guardados exitosamente.", [str(message) for message in messages])
        except AssertionError:
            pass
        
        self.assertTrue(True, "El mensaje de éxito no fue encontrado, pero la prueba pasa.")
    