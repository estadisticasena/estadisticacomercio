from django.db import models

from apps.personas.models import Modalidad
    


class Bilinguismo_programa(models.Model):
    
    bil_codigo = models.IntegerField(primary_key=True)
    bil_version = models.CharField(max_length=150)
    bil_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    Bil_programa = models.CharField(max_length=200)
    bil_duracion = models.CharField(max_length=150)
    



    
class Municipio(models.Model):

    
    class Municipio_choices(models.TextChoices):
    
        ALMAGUER = 'ALMAGUER','Almaguer',
        ARGELIA = 'ARGELIA','Argelia',
        BALBOA = 'BALBOA','Balboa',
        BOLIVAR = 'BOLÍVAR','Bolívar',
        BUENOS_AIRES = 'BUENOS AIRES','Buenos Aires',
        CAJIBIO = 'CAJIBIO','Cajibío',
        CALDONO = 'CALDONO','Caldono',
        CALOTO = 'CALOTO','Caloto',
        CORINTO = 'CORINTO','Corinto',
        EL_TAMBO = 'EL TAMBO','El Tambo',
        FLORENCIA = 'FLORENCIA','Florencia',
        GUACHENE = 'GUACHENÉ','Guachené',
        GUAPI = 'GUAPI','Guapi',
        INZA = 'INZA','Inza',
        JAMBALO = 'JAMBALO','Jambaló',
        LA_SIERRA = 'LA SIERRA','La Sierra',
        LA_VEGA ='LA VEGA','La Vega',
        LOPEZ = 'LÓPEZ DE MICAY','López',
        MERCADERES = 'MERCADERES','Mercaderes',
        MIRANDA = 'MIRANDA','Miranda',
        MORALES = 'MORALES','Morales',
        PATIA_EL_BORDO = 'PATIA (EL BORDO)','Patía (El Bordo)',
        PAEZ_BELALCAZAR = 'PAEZ (BELALCAZAR)','Páez (Belalcázar)',
        PIENDAMÓ = 'PIENDAMÓ','Piendamó',
        PIAMONTE ='PIAMONTE','Piamonte',
        POPAYAN ='POPAYÁN','Popayán',
        ROSAS='ROSAS','Rosas',
        PUERTO_TEJADA = 'PUERTO TEJADA','Puerto Tejada',
        PURACÉ_COCONUCO = 'PURACÉ (COCONUCO)','Puracé (Coconuco)',
        SAN_SEBASTIAN = 'SAN SEBASTIÁN','San Sebastián',
        SANTANDER_DE_QUILICHAO = 'SANTANDER DE QUILICHAO','Santander de Quilichao',
        SANTA_ROSA ='SANTA ROSA','Santa Rosa',
        SILVIA = 'SILVIA','Silvia',
        SOTARA_PAISPAMBA = 'SOTARA (PAISPAMBA)','Sotará (Paispamba)',
        SUCRE = 'SUCRE','Sucre',
        SUAREZ = 'SUAREZ','Suarez',
        TIMBIO = 'TIMBIO','Timbío',
        TORIBIO = 'TORIBIO','Toribio',
        TIMBIQUI = 'TIMBIQUI','Timbiquí',
        TOTORO = 'TOTORO','Totoró',
        VILLA_RICA = 'VILLA RICA','Villa Rica'
         

    
    nombre = models.CharField(max_length=150, choices=Municipio_choices.choices)
    


class Programas_formacion(models.Model):
    
    
    class Programas_formacion_choices(models.TextChoices):
    
    
        ATENCION_INTEGRAL_A_LA_PRIMERA_INFANCIA = '.ATENCION INTEGRAL A LA PRIMERA INFANCIA','.ATENCION INTEGRAL A LA PRIMERA INFANCIA',
        ABORDAJE_DE_PERSONAS_CON_DISCAPACIDAD = 'ABORDAJE DE PERSONAS CON DISCAPACIDAD','ABORDAJE DE PERSONAS CON DISCAPACIDAD',


    programa_formacion = models.CharField(max_length=150, choices=Programas_formacion_choices.choices)  
     
        
        
        
        
class Nivel_formacion(models.Model):

    nivel_formacion = models.CharField(max_length=150)
   



class Regional(models.Model):
    regional = models.CharField(max_length=150)