from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from apps.personas.models import Documento_vulnerables_poblaciones, Documento_vulnerables_tipo_poblaciones, Persona  # Ajustar según el proyecto
import json

class PoblacionVulnerableGraficasTests(TestCase):

    def setUp(self):
        # Configuración inicial de los datos de prueba
        self.cupos = 'Cupos'
        self.aprendices = 'Aprendices'
        self.persona = Persona.objects.create(per_documento='123456789')

        # Crear datos de prueba para Documento_vulnerables_poblaciones
        self.doc_cupos = Documento_vulnerables_poblaciones.objects.create(
            grupos_poblaciones=self.cupos, 
            porcentaje_ejecucion_poblaciones=Decimal('0.75'),
            ejecucion_poblaciones=Decimal('300'),
            meta_2024_poblaciones=Decimal('400'),
            per_documento=self.persona
        )
        self.doc_aprendices = Documento_vulnerables_poblaciones.objects.create(
            grupos_poblaciones=self.aprendices, 
            porcentaje_ejecucion_poblaciones=Decimal('0.50'),
            ejecucion_poblaciones=Decimal('200'),
            meta_2024_poblaciones=Decimal('500'),
            per_documento=self.persona
        )

        # Crear datos de prueba para Documento_vulnerables_tipo_poblaciones
        self.tipo_cupos = Documento_vulnerables_tipo_poblaciones.objects.create(
            grupo=self.cupos, 
            porcentaje_ejecucion=Decimal('0.80'),
            ejecucion=Decimal('160'),
            meta_2024=Decimal('200'),
            per_documento=self.persona
        )
        self.tipo_aprendices = Documento_vulnerables_tipo_poblaciones.objects.create(
            grupo=self.aprendices, 
            porcentaje_ejecucion=Decimal('0.60'),
            ejecucion=Decimal('120'),
            meta_2024=Decimal('200'),
            per_documento=self.persona
        )

    def test_poblacion_vulnerable_graficas_view(self):
        # Probar si la vista se carga correctamente
        response = self.client.get(reverse('personas:poblacion_vulnerable_graficas'))  # Ajusta el nombre de la URL si es necesario
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Poblacion_vulnerable/poblacion_vulnerable_graficas.html')

    def test_datos_grafica_poblacion(self):
        # Probar los datos de gráficos generados correctamente
        response = self.client.get(reverse('personas:poblacion_vulnerable_graficas'))

        # Verificar los datos de la gráfica para cupos y aprendices
        datos_grafica = json.loads(response.context['datos_grafica'])
        meta_grafica = json.loads(response.context['meta_grafica'])

        # Verificar valores en ejecuciones
        self.assertEqual(datos_grafica, ['300', '200'])  # Convertidos a cadenas
        self.assertEqual(meta_grafica, ['400', '500'])  # Metas de cupos y aprendices

    def test_conversion_porcentajes(self):
        # Verificar que los porcentajes se calculan correctamente
        response = self.client.get(reverse('personas:poblacion_vulnerable_graficas'))

        conversiones_cupos = response.context['conversiones_de_porcentajes_cupos']
        conversiones_aprendices = response.context['conversiones_de_porcentajes_aprendices']
        conversiones_cupos_tipo = response.context['conversiones_de_porcentajes_cupos_tipo_poblacion']
        conversiones_aprendices_tipo = response.context['conversiones_de_porcentajes_aprendices_tipo_poblacion']

        # Verificar valores de porcentajes
        self.assertEqual(conversiones_cupos, [75.0])  # 0.75 * 100
        self.assertEqual(conversiones_aprendices, [50.0])  # 0.50 * 100
        self.assertEqual(conversiones_cupos_tipo, [80.0])  # 0.80 * 100
        self.assertEqual(conversiones_aprendices_tipo, [60.0])  # 0.60 * 100

    def test_datos_grafica_tipo_poblacion(self):
        # Probar los datos de gráficos generados correctamente para tipo de poblaciones
        response = self.client.get(reverse('personas:poblacion_vulnerable_graficas'))

        data_tipo_poblaciones = json.loads(response.context['data_tipo_poblaciones'])
        meta_tipo_poblaciones = json.loads(response.context['meta_tipo_poblaciones'])

        # Verificar valores en ejecuciones y metas para tipo de poblaciones
        self.assertEqual(data_tipo_poblaciones, ['160', '120'])  # Ejecutados
        self.assertEqual(meta_tipo_poblaciones, ['200', '200'])  # Metas
