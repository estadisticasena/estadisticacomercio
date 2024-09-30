from django.test import TestCase
from django.urls import reverse
from apps.core.models import Bilinguismo_programa
from apps.personas.models import Modalidad

class BilinguismoTests(TestCase):
    def setUp(self):
        # Crear una instancia de Modalidad para usar en las pruebas
        self.modalidad = Modalidad.objects.create(
            modalidad='Presencial'  
        )
      
        # Crear un programa de bilingüismo para las pruebas
        self.bilinguismo = Bilinguismo_programa.objects.create(
            bil_codigo=1,
            bil_version='1.0',
            bil_modalidad=self.modalidad,
            Bil_programa='Programa de Bilingüismo',
            bil_duracion='6 meses'
        )

    def test_bilinguismo_index(self):
        # Hacer una solicitud GET a la vista Bilinguismo_index
        response = self.client.get(reverse('cores:bilinguismo_index'))

        # Verificar el código de estado de la respuesta
        self.assertEqual(response.status_code, 200)

        # Verificar que el contexto contenga los valores esperados
        self.assertIn('bilinguismo', response.context)
        self.assertIn('form_bilinguismo', response.context)

    def test_bilinguismo_create(self):
        # Hacer una solicitud POST para crear un nuevo programa de bilingüismo
        response = self.client.post(reverse('cores:bilinguismo_create'), {
            'bil_codigo': 6,  
            'bil_version': '2.0',
            'bil_modalidad': self.modalidad.id,  
            'Bil_programa': 'Nuevo Programa de Bilingüismo',
            'bil_duracion': '3 meses',
        })

        # Verificar que se redirige a la vista de índice de bilingüismo
        self.assertRedirects(response, reverse('cores:bilinguismo_index'))


        self.assertEqual(Bilinguismo_programa.objects.count(), 2) 

    def test_bilinguismo_edit(self):
        # Hacer una solicitud POST para editar un programa de bilingüismo existente
        response = self.client.post(reverse('cores:bilinguismo_edit', args=[self.bilinguismo.bil_codigo]), {
            'bil_version': '1.1',
            'bil_modalidad': self.modalidad.id,  # Usar la instancia creada
            'Bil_programa': 'Programa de Bilingüismo Editado',
            'bil_duracion': '6 meses',
        })

        # Verificar que se redirija a la vista de índice de bilingüismo
        self.assertRedirects(response, reverse('cores:bilinguismo_index'))

        # Verificar que los cambios se hayan guardado
        self.bilinguismo.refresh_from_db()
        self.assertEqual(self.bilinguismo.Bil_programa, 'Programa de Bilingüismo Editado')

    def test_bilinguismo_delete(self):
        # Hacer una solicitud POST para eliminar un programa de bilingüismo
        response = self.client.post(reverse('cores:bilinguismo_delete', args=[self.bilinguismo.bil_codigo]))

        # Verificar que se redirija a la vista de índice de bilingüismo
        self.assertRedirects(response, reverse('cores:bilinguismo_index'))

        # Verificar que el registro se haya eliminado
        self.assertEqual(Bilinguismo_programa.objects.count(), 0)  
