from django.test import TestCase
from django.urls import reverse
from apps.personas.models import Estrategia, Modalidad, Persona
from apps.core.models import Municipio
from apps.core.forms import Form_estrategias  # Asegúrate de que este formulario solo tenga los campos necesarios
from django.contrib.auth.models import User

class EstrategiasInstitutionalesTests(TestCase):
    
    def setUp(self):
        # Crear un usuario para autenticación si es necesario
        self.user = Persona.objects.create(per_documento='12345678')
        self.client.force_login(self.user)
        
        # Crear instancias necesarias para las pruebas
        self.modalidad = Modalidad.objects.create(modalidad='Presencial')
        self.estrategia = Estrategia.objects.create(est_nombre='Estrategia 1')

    def test_estrategias_institucionales_index(self):
        # Simula una solicitud GET a la vista Estrategias_institucionales_index
        response = self.client.get(reverse('cores:estrategias_institucionales_index'))

        # Verifica que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verifica que los formularios estén en el contexto
        self.assertIn('form_estrategias_institucionales', response.context)
        self.assertIn('form_meta', response.context)
        self.assertIn('form_meta_estrategia_detalle', response.context)
        
        # Verifica que los datos de estrategia estén en el contexto
        self.assertIn('estrategia', response.context)
        self.assertIn('modalidad', response.context)
        self.assertIn('detalle_estrategia', response.context)

        # Verifica que el template correcto haya sido renderizado
        self.assertTemplateUsed(response, 'Estrategias_institucionales/estrategias_institucionales.html')

    def test_estrategias_create(self):
        # Simula una solicitud POST para crear una nueva estrategia
        response = self.client.post(reverse('cores:estrategias_create'), {
            'est_nombre': 'Estrategia Nueva',
        })

        # Verifica que la respuesta redirija correctamente
        self.assertRedirects(response, reverse('cores:estrategias_institucionales_index'))

        # Verifica que la nueva estrategia haya sido creada en la base de datos
        self.assertTrue(Estrategia.objects.filter(est_nombre='Estrategia Nueva').exists())

    def test_estrategia_edit(self):
        # Simula una solicitud POST para editar una estrategia existente
        response = self.client.post(reverse('cores:estrategia_institucional_edit', args=[self.estrategia.est_id]), {
            'est_nombre': 'Estrategia Editada',
        })

        # Verifica que la respuesta redirija correctamente
        self.assertRedirects(response, reverse('cores:estrategias_institucionales_index'))

        # Verifica que la estrategia haya sido actualizada en la base de datos
        self.estrategia.refresh_from_db()
        self.assertEqual(self.estrategia.est_nombre, 'Estrategia Editada')
   
    def test_estrategia_delete(self):
        # Simula una solicitud POST para eliminar una estrategia existente
        response = self.client.post(reverse('cores:estrategia_institucional_delete', args=[self.estrategia.est_id]))

        # Verifica que la respuesta redirija correctamente
        self.assertRedirects(response, reverse('cores:estrategias_institucionales_index'))

        # Verifica que la estrategia haya sido eliminada de la base de datos
        self.assertFalse(Estrategia.objects.filter(est_id=self.estrategia.est_id).exists())
