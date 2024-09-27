from django.test import TestCase
from django.urls import reverse
from apps.core.models import Nivel_formacion  # Ajusta la importación según tu estructura
from apps.core.forms import Form_nivel_formacion  # Asegúrate de importar el formulario correcto

class NivelFormacionViewTests(TestCase):

    def setUp(self):
        # Crea una instancia de Nivel_formacion para usar en las pruebas
        self.nivel_formacion = Nivel_formacion.objects.create(nivel_formacion='Técnologo')

    def test_nivel_formacion_index(self):
        # Prueba que la vista de índice muestre correctamente los niveles de formación
        response = self.client.get(reverse('cores:nivel_formacion_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Nivel_formacion/nivel_formacion.html')
        self.assertContains(response, self.nivel_formacion.nivel_formacion)
        self.assertIn('nivel_formacion', response.context)

    def test_nivel_formacion_create(self):
        # Prueba la creación de un nuevo nivel de formación
        response = self.client.post(reverse('cores:nivel_formacion_create'), {
            'nivel_formacion': 'Técnico'
        })
        self.assertRedirects(response, reverse('cores:nivel_formacion_index'))
        self.assertTrue(Nivel_formacion.objects.filter(nivel_formacion='Técnico').exists())

    def test_nivel_formacion_edit(self):
        # Prueba la edición de un nivel de formación existente
        response = self.client.post(reverse('cores:nivel_formacion_edit', kwargs={'pk': self.nivel_formacion.pk}), {
            'nivel_formacion': 'Evento'
        })
        self.assertRedirects(response, reverse('cores:nivel_formacion_index'))
        self.nivel_formacion.refresh_from_db()  # Actualiza la instancia desde la base de datos
        self.assertEqual(self.nivel_formacion.nivel_formacion, 'Evento')

    def test_nivel_formacion_delete(self):
        # Prueba la eliminación de un nivel de formación existente
        response = self.client.post(reverse('cores:nivel_formacion_delete', kwargs={'pk': self.nivel_formacion.pk}))
        self.assertRedirects(response, reverse('cores:nivel_formacion_index'))
        self.assertFalse(Nivel_formacion.objects.filter(pk=self.nivel_formacion.pk).exists())
