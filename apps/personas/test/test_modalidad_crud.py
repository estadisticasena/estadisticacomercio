from django.test import TestCase
from django.urls import reverse
from apps.personas.models import Modalidad  # Asegúrate de que la importación sea correcta
from apps.core.forms import Form_modalidad  # Importa el formulario utilizado

class ModalidadViewTests(TestCase):

    def setUp(self):
        # Crea una instancia de Modalidad para usar en las pruebas
        self.modalidad = Modalidad.objects.create(modalidad='PRESENCIAL')

    def test_modalidad_index(self):
        # Prueba que la vista de index muestre correctamente las modalidades
        response = self.client.get(reverse('cores:modalidad_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Modalidad/modalidad_list.html')
        self.assertContains(response, self.modalidad.modalidad)
        self.assertIn('view_modalidades', response.context)

    def test_modalidad_create(self):
        # Prueba la creación de una nueva modalidad
        response = self.client.post(reverse('cores:modalidad_create'), {
            'modalidad': 'VIRTUAL'
        })
        self.assertRedirects(response, reverse('cores:modalidad_index'))
        self.assertTrue(Modalidad.objects.filter(modalidad='VIRTUAL').exists())

    def test_modalidad_edit(self):
        # Prueba la edición de una modalidad existente
        response = self.client.post(reverse('cores:modalidad_edit', kwargs={'pk': self.modalidad.pk}), {
            'modalidad': 'MODIFICADA'
        })
        self.assertRedirects(response, reverse('cores:modalidad_index'))
        self.modalidad.refresh_from_db()  # Actualiza la instancia de la base de datos
        self.assertEqual(self.modalidad.modalidad, 'MODIFICADA')

    def test_modalidad_delete(self):
        # Prueba la eliminación de una modalidad existente
        response = self.client.post(reverse('cores:modalidad_delete', kwargs={'pk': self.modalidad.pk}))
        self.assertRedirects(response, reverse('cores:modalidad_index'))
        self.assertFalse(Modalidad.objects.filter(pk=self.modalidad.pk).exists())

