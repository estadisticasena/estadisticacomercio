from django.test import TestCase
from django.urls import reverse
from apps.personas.models import P04, Centro_de_formacion
from apps.core.models import  Regional
from datetime import date
from faker import Faker
from django.utils import timezone
from django.contrib.auth import get_user_model
class DesercionViewTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()  # Crear una instancia de Faker
        
        # Crear un objeto Regional
        self.regional = Regional.objects.create(regional=self.fake.city())
        
        # Crear un objeto Centro de Formación
        self.centro_de_formacion = Centro_de_formacion.objects.create(centro_de_formacion=self.fake.company())
        User = get_user_model()  # Si estás usando un modelo de usuario personalizado
        self.persona = User.objects.create(
            per_documento=self.fake.random_int(min=1000000, max=99999999),  # Genera un documento aleatorio
            per_tipo_documento='CC',  # Ejemplo de tipo de documento
            email=self.fake.email(),
            per_nombres=self.fake.first_name(),
            per_apellidos=self.fake.last_name(),
            per_telefono=self.fake.phone_number()  # Genera un documento aleatorio
            # Agrega otros campos necesarios
        )
        # Crear objetos P04 con datos aleatorios
        for _ in range(10):  # Generar 10 registros de prueba
            P04.objects.create(
                fecha_p04=timezone.now(),
                codigo_regional=str(self.fake.random_int(min=1, max=999)).zfill(3),
  # Genera un código regional aleatorio
                nombre_regional=self.regional.regional,
                codigo_centro=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de centro aleatorio
                nombre_centro=self.centro_de_formacion.centro_de_formacion,
                identificador_ficha=self.fake.random_int(min=1, max=100),
                identificador_unico_ficha=self.fake.uuid4(),  # Genera un UUID único
                estado_curso=self.fake.random_element(elements=('Activo', 'Inactivo')),
                codigo_nivel_formacion=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de nivel aleatorio
                nivel_formacion=self.fake.random_element(elements=('Nivel 1', 'Nivel 2', 'Nivel 3')),
                fecha_inicio_ficha=self.fake.date_between(start_date='-1y', end_date='today'),
                fecha_terminacion_ficha=self.fake.date_between(start_date='today', end_date='+1y'),
                codigo_jornada=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de jornada aleatorio
                nombre_jornada=self.fake.random_element(elements=('Jornada Mañana', 'Jornada Tarde', 'Jornada Noche')),
                tipo_de_formacion=self.fake.random_element(elements=('Presencial', 'Virtual', 'Distancia')),
                etapa_ficha=self.fake.random_element(elements=('Etapa 1', 'Etapa 2')),
                modalidad_formacion=self.fake.random_element(elements=('Modalidad 1', 'Modalidad 2')),
                codigo_sector_programa=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de sector aleatorio
                nombre_sector_programa=self.fake.word(),
                codigo_ocupacion=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de ocupación aleatorio
                nombre_ocupacion=self.fake.word(),
                codigo_programa=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de programa aleatorio
                version_programa=self.fake.random_element(elements=('V1', 'V2', 'V3')),
                nombre_programa_formacion=self.fake.word(),
                codigo_pais_curso='COL',  # Asumimos que es Colombia
                nombre_pais_curso='Colombia',
                codigo_departamento_curso=str(self.fake.random_int(min=1, max=999)).zfill(3),# Genera un código de departamento aleatorio
                nombre_departamento_curso=self.fake.word(),
                codigo_municipio_curso=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de municipio aleatorio
                nombre_municipio_curso=self.fake.word(),
                codigo_convenio=str(self.fake.random_int(min=1, max=999)).zfill(3), # Genera un código de convenio aleatorio
                nombre_convenio=self.fake.word(),
                ampliacion_cobertura=self.fake.word(),
                codigo_programa_especial=str(self.fake.random_int(min=1, max=999)).zfill(3),  # Genera un código de programa especial aleatorio
                nombre_programa_especial=self.fake.word(),
                numero_cursos=self.fake.random_int(min=1, max=10),
                total_aprendices=self.fake.random_int(min=50, max=150),  # Número aleatorio entre 50 y 150
                total_aprendices_activos=self.fake.random_int(min=0, max=150),  # Número aleatorio entre 0 y 150
                duracion_programa=self.fake.random_element(elements=('3 meses', '6 meses', '1 año')),
                nombre_nuevo_sector=self.fake.word(),
                per_documento=self.persona # Asegúrate de que esto sea un objeto Persona válido
            )

    def test_desercion_view_with_filters(self):
        response = self.client.get(reverse('cores:Desercion'), {
            'id_modalidad': '1',  # Aquí 1 corresponde a 'PRESENCIAL'
           # Usa un municipio aleatorio creado
            'regional': self.regional.id,
            'centro_de_formacion': self.centro_de_formacion.id,
            'fecha_inicio_ficha': date.today().strftime('%Y-%m-%d'),
            'fecha_terminacion_ficha': (date.today().replace(year=date.today().year + 1)).strftime('%Y-%m-%d'),
        })

        self.assertEqual(response.status_code, 200)

        context = response.context
        # Verificar los resultados
        total_aprendices = sum(p.total_aprendices for p in P04.objects.all())
        total_activos = sum(p.total_aprendices_activos for p in P04.objects.all())

        self.assertEqual(context['aprendices_activos'], total_activos)  # Verifica que el total de activos sea correcto
        self.assertEqual(context['deserciones'], total_aprendices - total_activos)  # Verifica el cálculo de deserciones
