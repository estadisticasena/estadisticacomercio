from datetime import date
from django.test import TestCase
from django.urls import reverse
from apps.personas.models import P04, Centro_de_formacion, Persona,Programa
from apps.core.models import Regional, Nivel_formacion
from django.utils import timezone

class ProgramaViewTestCase(TestCase):
    
    def setUp(self):
        # Configura datos de prueba aquí, como crear instancias de modelos necesarios
        self.regional = Regional.objects.create(regional='REGIONAL CAUCA')
        self.centro_de_formacion = Centro_de_formacion.objects.create(centro_de_formacion='CENTRO DE COMERCIO Y SERVICIOS')
        self.nivel_formacion = Nivel_formacion.objects.create(nivel_formacion='CURSO ESPECIAL')

        # Crea una persona de prueba
        self.persona = Persona.objects.create(per_documento='12345678')  

        # Crea un registro en el modelo P04
        self.p04 = P04.objects.create(
            fecha_p04=timezone.now(),
            codigo_regional='REG001',
            nombre_regional='REGIONAL CAUCA',
            codigo_centro='CEN001',
            nombre_centro='CENTRO DE COMERCIO Y SERVICIOS',
            identificador_ficha=1,
            identificador_unico_ficha='UNIQUE_ID_001',
            estado_curso='Activo',
            codigo_nivel_formacion='NIV001',
            nivel_formacion=self.nivel_formacion,
            fecha_inicio_ficha=date(2024, 1, 1),
            fecha_terminacion_ficha=date(2024, 12, 31),
            codigo_jornada='JORN001',
            nombre_jornada='Jornada Name',
            tipo_de_formacion='Presencial',
            etapa_ficha='Etapa 1',
            modalidad_formacion='PRESENCIAL',
            codigo_sector_programa='SEC001',
            nombre_sector_programa='Sector Name',
            codigo_ocupacion='OCC001',
            nombre_ocupacion='Occupation Name',
            codigo_programa='PROG001',
            version_programa='V1',
            nombre_programa_formacion='Program Name',
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
            total_aprendices_activos=80,
            duracion_programa='6 meses',
            nombre_nuevo_sector='Nuevo Sector',
            per_documento=self.persona  # Asegúrate de que esto sea un objeto Persona válido
        )
        
    def test_programa_view_with_filters(self):
        response = self.client.get(reverse('cores:programa'), {
            'centro_de_formacion': self.centro_de_formacion.id,
            'nivel_formacion': self.nivel_formacion.id,
            'programa_formacion': 'Program Name',  # Cambia según tu lógica
            'modalidad': '1',  # Presencial
        })
        
        # Imprimir el contexto para verificar qué datos se están pasando
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('programa_formacion', context)
        self.assertEqual(context['selected_nivel_formacion'], self.nivel_formacion.id)
        self.assertEqual(context['selected_centro_de_formacion'], self.centro_de_formacion.id)
        self.assertIn('lista_municipios', context)
        self.assertIn('lista_fichas', context)

    def test_programa_view_with_no_filters(self):
        """Prueba la vista de programa sin filtros aplicados."""
        response = self.client.get(reverse('cores:programa'))

        # Verifica que la respuesta es correcta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Programa/programa.html')

        # Verifica que se están proporcionando datos por defecto
        context = response.context
        self.assertIn('centro_de_formacion', context)
        self.assertIn('nivel_formacion', context)
        self.assertIn('programa_formacion', context)
        self.assertIn('modalidad', context)
