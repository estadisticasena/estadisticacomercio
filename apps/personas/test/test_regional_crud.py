from django.test import TestCase
from django.urls import reverse
from apps.core.models import Regional  
from apps.core.forms import Form_regional 

class RegionalViewTests(TestCase):

    def setUp(self):
        # Crea una instancia de Regional para usar en las pruebas
        self.regional = Regional.objects.create(regional='Antioquia')

    def test_regional_index(self):
        # Prueba que la vista de índice muestre correctamente las regiones
        response = self.client.get(reverse('cores:regional_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Regional/regional.html')
        self.assertContains(response, self.regional.regional)
        self.assertIn('regional', response.context)

    def test_regional_create(self):
        # Prueba la creación de una nueva región
        response = self.client.post(reverse('cores:regional_create'), {
            'regional': 'Cundinamarca'
        })
        self.assertRedirects(response, reverse('cores:regional_index'))
        self.assertTrue(Regional.objects.filter(regional='Cundinamarca').exists())

    def test_regional_edit(self):
        # Prueba la edición de una región existente
        response = self.client.post(reverse('cores:regional_edit', kwargs={'pk': self.regional.pk}), {
            'regional': 'Santander'
        })
        self.assertRedirects(response, reverse('cores:regional_index'))
        self.regional.refresh_from_db()  # Actualiza la instancia desde la base de datos
        self.assertEqual(self.regional.regional, 'Santander')

    def test_regional_delete(self):
        # Prueba la eliminación de una región existente
        response = self.client.post(reverse('cores:regional_delete', kwargs={'pk': self.regional.pk}))
        self.assertRedirects(response, reverse('cores:regional_index'))
        self.assertFalse(Regional.objects.filter(pk=self.regional.pk).exists())
