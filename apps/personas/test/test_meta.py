from django.test import TestCase
from django.urls import reverse

from apps.personas.models import Persona,Meta


class MetaTests(TestCase):
    def setUp(self):
        # Crear una instancia de Persona para usar en las pruebas
        self.usuario = Persona.objects.create(
            per_documento='123456789',  # Ajusta esto según el campo que uses
            # Agrega otros campos necesarios para la creación del usuario
        )
        self.client.force_login(self.usuario)  # Iniciar sesión como usuario

        # Crear una instancia de Meta para usar en las pruebas
        self.meta = Meta.objects.create(
            met_codigo='Código de prueba',
            met_fecha_inicio='2024-01-01',
            met_fecha_fin='2024-12-31',
            met_año='2024',
            met_total_otras_poblaciones='100',
            met_total_victimas='50',
            met_total_hechos_victimizantes='10',
            met_total_desplazados_violencia='5',
            met_total_titulada='20',
            met_total_complementaria='30',
            met_total_poblacion_vulnerable='15',
            per_documento=self.usuario  # Relacionar con el usuario creado
        )

    def test_meta_create(self):
        # Descripción: Simula una solicitud POST para crear una nueva meta con datos válidos.
        # Resultado esperado: Se espera que el sistema redirija al usuario a la vista de índice de metas y que se haya creado un nuevo registro en la base de datos.
        
        response = self.client.post(reverse('cores:meta_create'), {
            'met_codigo': 'Código nuevo',
            'met_fecha_inicio': '2024-02-01',
            'met_fecha_fin': '2024-11-30',
            'met_año': '2024',
            'met_total_otras_poblaciones': '150',
            'met_total_victimas': '60',
            'met_total_hechos_victimizantes': '20',
            'met_total_desplazados_violencia': '10',
            'met_total_titulada': '25',
            'met_total_complementaria': '35',
            'met_total_poblacion_vulnerable': '20',
            'per_documento': self.usuario.per_documento  # Relacionar con el usuario creado
        })

        # Verificar que se redirige a la vista de índice de metas
        self.assertRedirects(response, reverse('cores:meta_index'))

        # Verificar que se haya creado un nuevo registro
        self.assertEqual(Meta.objects.count(), 2)  # Debe haber 2 registros ahora

    def test_meta_delete(self):
        # Descripción: Simula una solicitud POST para eliminar una meta existente.
        # Resultado esperado: Se espera que el sistema redirija al usuario a la vista de índice de metas y que el registro se haya eliminado de la base de datos.
        
        response = self.client.post(reverse('cores:meta_delete', args=[self.meta.met_id]))

        # Verificar que se redirige a la vista de índice de metas
        self.assertRedirects(response, reverse('cores:meta_index'))

        # Verificar que el registro se haya eliminado
        self.assertEqual(Meta.objects.count(), 0)  # Debería quedar 0 registros

    def test_meta_index(self):
        # Descripción: Simula una solicitud GET a la vista de índice de metas.
        # Resultado esperado: Se espera que la respuesta tenga un código de estado 200 y que el contexto contenga las claves 'view_metas', 'form_meta', y 'form'.
        
        response = self.client.get(reverse('cores:meta_index'))

        # Verificar el código de estado de la respuesta
        self.assertEqual(response.status_code, 200)

        # Verificar que el contexto contenga los valores esperados
        self.assertIn('view_metas', response.context)
        self.assertIn('form_meta', response.context)

    def test_meta_edit(self):
        # Descripción: Simula una solicitud POST para editar una meta existente.
        # Resultado esperado: Se espera que el sistema redirija al usuario a la vista de índice de metas y que los cambios realizados en la meta se reflejen en la base de datos.

        response = self.client.post(reverse('cores:meta_edit', args=[self.meta.met_id]), {
            'met_codigo': 'Código editado',
            'met_fecha_inicio': '2024-01-01',
            'met_fecha_fin': '2024-12-31',
            'met_año': '2024',
            'met_total_otras_poblaciones': '200',
            'met_total_victimas': '70',
            'met_total_hechos_victimizantes': '30',
            'met_total_desplazados_violencia': '15',
            'met_total_titulada': '35',
            'met_total_complementaria': '45',
            'met_total_poblacion_vulnerable': '25',
            'per_documento': self.usuario.per_documento  # Relacionar con el usuario creado
        })

        # Verificar que se redirige a la vista de índice de metas
        self.assertRedirects(response, reverse('cores:meta_index'))

        # Verificar que los cambios se han guardado en la base de datos
        self.meta.refresh_from_db()  # Refrescar los datos desde la base de datos
        self.assertEqual(self.meta.met_codigo, 'Código editado')
        self.assertEqual(self.meta.met_total_otras_poblaciones, '200')
