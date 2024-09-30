from django.test import TestCase
from django.http import HttpRequest
from django.urls import reverse
from apps.personas.models import P04, Persona, Centro_de_formacion
from datetime import date
from django.utils import timezone


class GeneralViewTestCase(TestCase):
    def setUp(self):
        # Crear instancias de prueba de tus modelos
        self.centro_formacion = Centro_de_formacion.objects.create(centro_de_formacion='CENTRO DE COMERCIO Y SERVICIOS')
        self.persona = Persona.objects.create(per_documento='12345678')  
        self.p04 = P04.objects.create(
            nombre_centro=self.centro_formacion,
            modalidad_formacion='PRESENCIAL',
            fecha_p04=timezone.now(),
            codigo_regional='REG001',
            nombre_regional='REGIONAL CAUCA',
            codigo_centro='CEN001',
            identificador_ficha=1,
            identificador_unico_ficha='UNIQUE_ID_001',
            estado_curso='Activo',
            codigo_nivel_formacion='NIV001',
            nivel_formacion='TECNÓLOGO',
            fecha_inicio_ficha=date(2024, 1, 1),
            fecha_terminacion_ficha=date(2024, 12, 31),
            codigo_jornada='JORN001',
            nombre_jornada='Jornada Name',
            tipo_de_formacion='Presencial',
            etapa_ficha='Etapa 1',
            codigo_sector_programa='SEC001',
            nombre_sector_programa='Sector Name',
            codigo_ocupacion='OCC001',
            nombre_ocupacion='Occupation Name',
            codigo_programa='PROG001',
            version_programa='V1',
            nombre_programa_formacion='INGLES BASICO - NIVEL 1',
            codigo_pais_curso='COL',
            nombre_pais_curso='Colombia',
            codigo_departamento_curso='DEP001',
            nombre_departamento_curso='Department Name',
            codigo_municipio_curso='MUN001',
            nombre_municipio_curso='ALMAGUER',
            codigo_convenio='CONV001',
            nombre_convenio='Convenio Name',
            ampliacion_cobertura='Ampliación 1',
            codigo_programa_especial='PROG_ESPECIAL001',
            nombre_programa_especial='Programa Especial',
            numero_cursos='5',
            total_aprendices=100,
            total_aprendices_activos=10,
            duracion_programa='6 meses',
            nombre_nuevo_sector='Nuevo Sector',
            per_documento=self.persona
        )

    def test_general_view(self):
        # Hacer una solicitud GET usando el cliente de pruebas
        response = self.client.get(reverse('cores:general'), {
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-12-31',
            'id_centro_de_formacion': self.centro_formacion.id,
        })

        # Verificar el código de estado de la respuesta
        self.assertEqual(response.status_code, 200)

        # Verificar que el contexto contenga los valores esperados
        self.assertIn('labels_presenciales', response.context)
        self.assertIn('data', response.context)

        # Verificar valores específicos en el contexto
        expected_data = [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
        self.assertListEqual(response.context['data'], expected_data) 