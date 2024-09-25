from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.personas.models import P04, Centro_de_formacion, Persona
from apps.core.models import Municipio
from collections import Counter
from datetime import timedelta
class CoberturaMapaViewTestCase(TestCase):
    
    def setUp(self):
        # Crea instancias de prueba para centros de formación, municipios, personas y P04
        self.municipio = Municipio.objects.create(nombre='ALMAGUER')
        self.centro_de_formacion = Centro_de_formacion.objects.create(centro_de_formacion='CENTRO DE COMERCIO Y SERVICIOS')
        self.persona = Persona.objects.create(per_documento=1234567890)  
        
        # Crear registros de prueba en P04
        self.p04 = P04.objects.create(
            
            
          
            fecha_p04=timezone.now(),
            codigo_regional='REG001',
            nombre_regional='REGIONAL CAUCA',
            codigo_centro='CEN001',
            nombre_centro=self.centro_de_formacion.centro_de_formacion,
            identificador_ficha=1,
            identificador_unico_ficha='UNIQUE_ID_001',
            estado_curso='Activo',
            codigo_nivel_formacion='NIV001',
            nivel_formacion='Nivel 1',
            fecha_inicio_ficha=timezone.now().date() - timedelta(days=10),  # Fecha dentro del rango
            fecha_terminacion_ficha=timezone.now().date() + timedelta(days=10), 
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
            nombre_municipio_curso=self.municipio.nombre,
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
            per_documento=self.persona 
        )
    
    def test_cobertura_view_renders_correct_template(self):
        """Prueba que la vista utilice la plantilla correcta."""
        response = self.client.get(reverse('cores:cobertura_mapa'))  # Ajusta el nombre de la URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Cobertura/cobertura.html')

    def test_cobertura_view_filters_by_municipio(self):
        """Prueba el filtro por municipio."""
        response = self.client.get(reverse('cores:cobertura_mapa'), {
            'nombre_municipio': 'ALMAGUER'
        })
        self.assertEqual(response.status_code, 200)
        
        # Verifica que el filtro funcione correctamente
        programas_conteo = response.context['programas_conteo']
        self.assertIn(('Program Name', 'Nivel 1'), programas_conteo)

    def test_cobertura_view_filters_by_fecha_inicio_and_fin(self):
        """Prueba el filtro por rango de fechas."""
        selected_fecha_inicio = '2024-09-03'
        selected_fecha_fin = '2024-12-01'

        response = self.client.get(reverse('cores:cobertura_mapa'), {
            'filtroFechaInicio': selected_fecha_inicio,
            'filtroFechaFin': selected_fecha_fin
        })
        self.assertEqual(response.status_code, 200)

        # Verifica que los registros de P04 dentro del rango de fechas estén presentes
        programas_conteo = response.context['programas_conteo']
        self.assertGreater(len(programas_conteo), 0)

    def test_cobertura_view_filters_by_centro_de_formacion(self):
        """Prueba el filtro por centro de formación."""
        response = self.client.get(reverse('cores:cobertura_mapa'), {
            'id_centro_de_formacion': self.centro_de_formacion.id
        })
        self.assertEqual(response.status_code, 200)

        # Verifica que el filtro funcione correctamente
        programas_conteo = response.context['programas_conteo']
        self.assertIn(('Program Name', 'Nivel 1'), programas_conteo)

    def test_cobertura_view_with_all_filters(self):
        """Prueba la vista con todos los filtros aplicados."""
        response = self.client.get(reverse('cores:cobertura_mapa'), {
            'nombre_municipio': 'ALMAGUER',
            'filtroFechaInicio': '2024-09-03',
            'filtroFechaFin': '2024-12-01',
            'id_centro_de_formacion': self.centro_de_formacion.id
        })
        self.assertEqual(response.status_code, 200)

        # Verifica que el filtro funcione correctamente
        programas_conteo = response.context['programas_conteo']
        self.assertIn(('Program Name', 'Nivel 1'), programas_conteo)

    def test_cobertura_view_handles_empty_results(self):
        """Prueba que la vista maneje correctamente cuando no hay resultados."""
        response = self.client.get(reverse('cores:cobertura_mapa'), {
            'nombre_municipio': 'Nonexistent Municipio',
            'filtroFechaInicio': '2023-01-01',
            'filtroFechaFin': '2024-01-01'
        })
        self.assertEqual(response.status_code, 200)

        # Verifica que no haya resultados en el contexto
        programas_conteo = response.context['programas_conteo']
        self.assertEqual(len(programas_conteo), 0)
