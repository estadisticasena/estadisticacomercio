# Generated by Django 5.0.5 on 2024-09-19 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bilinguismo_programa',
            fields=[
                ('bil_codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('bil_version', models.CharField(max_length=150)),
                ('Bil_programa', models.CharField(max_length=200)),
                ('bil_duracion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('ALMAGUER', 'Almaguer'), ('ARGELIA', 'Argelia'), ('BALBOA', 'Balboa'), ('BOLÍVAR', 'Bolívar'), ('BUENOS AIRES', 'Buenos Aires'), ('CAJIBIO', 'Cajibío'), ('CALDONO', 'Caldono'), ('CALOTO', 'Caloto'), ('CORINTO', 'Corinto'), ('EL TAMBO', 'El Tambo'), ('FLORENCIA', 'Florencia'), ('GUACHENÉ', 'Guachené'), ('GUAPI', 'Guapi'), ('INZA', 'Inza'), ('JAMBALO', 'Jambaló'), ('LA SIERRA', 'La Sierra'), ('LA VEGA', 'La Vega'), ('LÓPEZ DE MICAY', 'López'), ('MERCADERES', 'Mercaderes'), ('MIRANDA', 'Miranda'), ('MORALES', 'Morales'), ('PATIA (EL BORDO)', 'Patía (El Bordo)'), ('PAEZ (BELALCAZAR)', 'Páez (Belalcázar)'), ('PIENDAMÓ', 'Piendamó'), ('PIAMONTE', 'Piamonte'), ('POPAYÁN', 'Popayán'), ('ROSAS', 'Rosas'), ('PUERTO TEJADA', 'Puerto Tejada'), ('PURACÉ (COCONUCO)', 'Puracé (Coconuco)'), ('SAN SEBASTIÁN', 'San Sebastián'), ('SANTANDER DE QUILICHAO', 'Santander de Quilichao'), ('SANTA ROSA', 'Santa Rosa'), ('SILVIA', 'Silvia'), ('SOTARA (PAISPAMBA)', 'Sotará (Paispamba)'), ('SUCRE', 'Sucre'), ('SUAREZ', 'Suarez'), ('TIMBIO', 'Timbío'), ('TORIBIO', 'Toribio'), ('TIMBIQUI', 'Timbiquí'), ('TOTORO', 'Totoró'), ('VILLA RICA', 'Villa Rica')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel_formacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel_formacion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Programas_formacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programa_formacion', models.CharField(choices=[('.ATENCION INTEGRAL A LA PRIMERA INFANCIA', '.ATENCION INTEGRAL A LA PRIMERA INFANCIA'), ('ABORDAJE DE PERSONAS CON DISCAPACIDAD', 'ABORDAJE DE PERSONAS CON DISCAPACIDAD')], max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Regional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regional', models.CharField(max_length=150)),
            ],
        ),
    ]
