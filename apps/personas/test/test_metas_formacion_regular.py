from django.test import TestCase
from django.urls import reverse
from apps.personas.models import Metas_formacion, Centro_de_formacion, Modalidad, Meta, Persona
from datetime import date
from unittest.mock import patch 
from apps.core.views import Meta_formacion_edit 
from django.http import HttpResponseRedirect
class MetaFormacionTests(TestCase):

    def setUp(self):
        self.centro_formacion = Centro_de_formacion.objects.create(
            centro_de_formacion='Centro 1',
        )
        self.modalidad = Modalidad.objects.create(
            modalidad='Presencial',
        )
        self.usuario = Persona.objects.create(
            per_documento='123456789',
          
        )
        self.meta = Meta.objects.create(
            met_codigo='1214',
            met_fecha_inicio=date(2024, 1, 1),
            met_fecha_fin=date(2024, 12, 31),
            met_año='2024',
            met_total_otras_poblaciones='123',
            met_total_victimas='123',
            met_total_hechos_victimizantes='123',
            met_total_desplazados_violencia='123',
            met_total_complementaria='123',
            met_total_poblacion_vulnerable='123',
            per_documento=self.usuario,
        )

        # Crear una meta de formación de prueba
        self.meta_formacion = Metas_formacion.objects.create(
            metd_modalidad=self.modalidad,
            met_formacion_operario=10,
            met_formacion_auxiliar=20,
            met_centro_formacion=self.centro_formacion,
            met_formacion_tecnico=15,
            met_formacion_profundizacion_tecnica=5,
            met_formacion_tecnologo=25,
            met_formacion_evento=30,
            met_formacion_curso_especial=40,
            met_formacion_bilinguismo=12,
            met_formacion_sin_bilinguismo=8,
            met_id=self.meta
        )

    def test_meta_formacion_create(self):
        # Crear un nuevo centro de formación para la prueba
        centro_formacion_nuevo = Centro_de_formacion.objects.create(
            centro_de_formacion='Centro 2'
        )
        # Simula una solicitud POST para crear una nueva meta de formación
        response = self.client.post(reverse('cores:meta_formacion_create'), {
            'metd_modalidad': self.modalidad.id, 
            'met_formacion_operario': 1,
            'met_formacion_auxiliar': 10,
            'met_centro_formacion': centro_formacion_nuevo.id, 
            'met_formacion_tecnico': 12,
            'met_formacion_profundizacion_tecnica': 3,
            'met_formacion_tecnologo': 20,
            'met_formacion_evento': 25,
            'met_formacion_curso_especial': 35,
            'met_formacion_bilinguismo': 15,
            'met_formacion_sin_bilinguismo': 10,
            'met_id': self.meta.met_id  
        })

        # Verifica que la meta de formación se haya creado
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Metas_formacion.objects.filter(met_centro_formacion=centro_formacion_nuevo).exists())



    @patch.object(Meta_formacion_edit, 'dispatch')
    def test_meta_formacion_edit(self, mock_dispatch):
        # Configura el mock para que devuelva una respuesta de redirección
        mock_dispatch.return_value = HttpResponseRedirect(reverse('cores:formacion_regular_index'))

 
        response = self.client.post(reverse('cores:meta_formacion_regular_edit', args=[self.meta_formacion.metd_id]), {
            'metd_modalidad': self.modalidad.id,  # Usar la modalidad existente
            'met_formacion_operario': 10,  # Valor nuevo que quieres establecer
            'met_formacion_auxiliar': 10,
            'met_centro_formacion': self.centro_formacion.id,  # Referencia por ID
            'met_formacion_tecnico': 12,
            'met_formacion_profundizacion_tecnica': 3,
            'met_formacion_tecnologo': 20,
            'met_formacion_evento': 25,
            'met_formacion_curso_especial': 35,
            'met_formacion_bilinguismo': 15,
            'met_formacion_sin_bilinguismo': 10,
            'met_id': self.meta_formacion.met_id 
        })
        self.meta_formacion.refresh_from_db()
        # Verifica que la respuesta redirija correctamente
        self.assertRedirects(response, reverse('cores:formacion_regular_index'))

       
        self.assertEqual(self.meta_formacion.met_formacion_operario, 10)  
    def test_meta_formacion_delete(self):
        # Simula una solicitud POST para eliminar una meta de formación
        response = self.client.post(reverse('cores:meta_formacion_regular_delete', args=[self.meta_formacion.metd_id]))
        
        # Verifica que la meta de formación haya sido eliminada
        self.assertEqual(response.status_code, 302)  # Redirección exitosa
        self.assertFalse(Metas_formacion.objects.filter(metd_id=self.meta_formacion.metd_id).exists())

    

    def test_formacion_regular_index(self):
        # Simula una solicitud GET a la vista Formacion_regular_index
        response = self.client.get(reverse('cores:formacion_regular_index'))

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verifica que los formularios estén en el contexto
        self.assertIn('form', response.context)
        self.assertIn('form_meta_formacion', response.context)
        
        # Verifica que el template correcto haya sido renderizado
        self.assertTemplateUsed(response, 'Formacion_regular/formacion_regular.html')
