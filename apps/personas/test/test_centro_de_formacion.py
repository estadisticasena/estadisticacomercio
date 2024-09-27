from django.test import TestCase
from django.urls import reverse
from apps.personas.models import Centro_de_formacion  # Ajusta la importación según tu estructura
from apps.core.forms import Form_centro_de_formacion  # Asegúrate de importar el formulario correcto

class CentroDeFormacionViewTests(TestCase):

    def setUp(self):
        # Crea una instancia de Centro_de_formacion para usar en las pruebas
        self.centro_de_formacion = Centro_de_formacion.objects.create(centro_de_formacion='Centro ABC')

    def test_centro_de_formacion_index(self):
        # Prueba que la vista de índice muestre correctamente los centros de formación
        response = self.client.get(reverse('cores:centro_de_formacion_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Centro_de_formacion/centro_de_formacion.html')
        self.assertContains(response, self.centro_de_formacion.centro_de_formacion)
        self.assertIn('centro_de_formacion', response.context)

    def test_centro_de_formacion_create(self):
        # Prueba la creación de un nuevo centro de formación
        response = self.client.post(reverse('cores:centro_de_formacion_create'), {
            'centro_de_formacion': 'Centro DEF'
        })
        self.assertRedirects(response, reverse('cores:centro_de_formacion_index'))
        self.assertTrue(Centro_de_formacion.objects.filter(centro_de_formacion='Centro DEF').exists())

    def test_centro_de_formacion_edit(self):
        # Prueba la edición de un centro de formación existente
        response = self.client.post(reverse('cores:centro_de_formacion_edit', kwargs={'pk': self.centro_de_formacion.pk}), {
            'centro_de_formacion': 'Centro Modificado'
        })
        self.assertRedirects(response, reverse('cores:centro_de_formacion_index'))
        self.centro_de_formacion.refresh_from_db()  # Actualiza la instancia desde la base de datos
        self.assertEqual(self.centro_de_formacion.centro_de_formacion, 'Centro Modificado')

    def test_centro_de_formacion_delete(self):
        # Prueba la eliminación de un centro de formación existente
        response = self.client.post(reverse('cores:centro_de_formacion_delete', kwargs={'pk': self.centro_de_formacion.pk}))
        self.assertRedirects(response, reverse('cores:centro_de_formacion_index'))
        self.assertFalse(Centro_de_formacion.objects.filter(pk=self.centro_de_formacion.pk).exists())
