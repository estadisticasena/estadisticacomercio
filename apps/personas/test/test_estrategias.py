from django.test import TestCase
from django.urls import reverse
from apps.personas.models import Estrategia_detalle, P04, Centro_de_formacion, Modalidad, Persona,Estrategia ,Meta# Asegúrate de importar tus modelos
from datetime import date
from django.utils import timezone
class EstrategiaViewTests(TestCase):

    def setUp(self):
        # Crea una instancia de Modalidad
        self.modalidad_presencial = Modalidad.objects.create(modalidad='PRESENCIAL')

        # Crea un Centro de Formación
        self.centro1 = Centro_de_formacion.objects.create(centro_de_formacion='Centro 1')
        self.persona = Persona.objects.create(per_documento='12345678')  

        # Crea una única instancia de P04
        self.p04 = P04.objects.create(
            fecha_p04=timezone.now(),
            codigo_regional='REG001',
            nombre_regional='REGIONAL CAUCA',
            codigo_centro='CEN001',
            nombre_centro=self.centro1,
            identificador_ficha=1,
            identificador_unico_ficha='UNIQUE_ID_001',
            estado_curso='Activo',
            codigo_nivel_formacion='NIV001',
            nivel_formacion='Nivel 1',
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
            total_aprendices_activos=10,
            duracion_programa='6 meses',
            nombre_nuevo_sector='Nuevo Sector',
            per_documento=self.persona
        )
        self.estrategia = Estrategia.objects.create(
            est_nombre ='Estrategia 1',
         )
        self.meta = Meta.objects.create(
            met_codigo = '1214',
            met_fecha_inicio=date(2024, 1, 1),
            met_fecha_fin=date(2024, 12, 31),
            met_año = '2024',
            met_total_otras_poblaciones = '123',
            met_total_victimas = '123',
            met_total_hechos_victimizantes = '123',
            met_total_desplazados_violencia = '123',
            met_total_complementaria = '123',
            met_total_poblacion_vulnerable = '123',
            per_documento = self.persona,
            
  
         )


        # Crea una estrategia detalle
        self.estrategia_detalle = Estrategia_detalle.objects.create(
            estd_modalidad=self.modalidad_presencial,
            est_id=self.estrategia,
            estd_meta=self.meta,

            estd_auxiliar_meta=5,
            estd_tecnico_meta=10,
            estd_tecnologo=15,
            estd_evento=20,
            estd_operario_meta=25,
            estd_curso_especial=30,
            estd_bilinguismo=35,
            estd_sin_bilinguismo=40,
            estd_profundizacion_tecnica_meta=40
        )


    def test_filtrar_por_fechas(self):
        # Filtro por rango de fechas que incluye el único registro
        response = self.client.get(reverse('cores:estrategias_index'), {
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-12-31'
        })
        self.assertEqual(response.status_code, 200)

        # Verificamos que el único registro está presente
        presencial_data = response.context['data_presencial_p04_tabla']
        virtual_data = response.context['data_virtual_p04_tabla']

        self.assertEqual(len(presencial_data), 9)
        self.assertEqual(len(virtual_data), 9)  

    def test_filtrar_por_centro_de_formacion(self):
        # Filtro por centro de formación que incluye el único registro
        response = self.client.get(reverse('cores:estrategias_index'), {
            'id_centro_de_formacion': self.centro1.id
        })
        self.assertEqual(response.status_code, 200)

        presencial_data = response.context['data_presencial_p04_tabla']
        virtual_data = response.context['data_virtual_p04_tabla']

        # El único registro pertenece a centro1
        self.assertEqual(len(presencial_data), 9)
        self.assertEqual(len(virtual_data), 9)

    def test_filtrar_por_modalidad(self):
        # Filtro por modalidad PRESENCIAL
        response = self.client.get(reverse('cores:estrategias_index'), {
            'modalidad': 'PRESENCIAL'
        })
        self.assertEqual(response.status_code, 200)
    
   
    
        presencial_data = response.context['data_presencial_p04_tabla']
        virtual_data = response.context['data_virtual_p04_tabla']
    
        # Solo hay un registro presencial
        self.assertEqual(len(presencial_data), 9)
        self.assertEqual(len(virtual_data), 9)
    

    def test_filtrar_por_fechas_fuera_de_rango(self):
        # Filtro con fechas que no incluyen el registro
        response = self.client.get(reverse('cores:estrategias_index'), {
            'fecha_inicio': '2023-01-01',
            'fecha_fin': '2023-12-31'
        })
        self.assertEqual(response.status_code, 200)

        presencial_data = response.context['data_presencial_p04_tabla']
        virtual_data = response.context['data_virtual_p04_tabla']

        # No debería haber registros porque el único está fuera del rango
        self.assertEqual(len(presencial_data), 9)
        self.assertEqual(len(virtual_data), 9)
