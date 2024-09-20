from django.forms import BaseModelForm
from django.shortcuts import render
from apps.personas.models import P04,Meta,Persona,Modalidad,Metas_formacion,Estrategia, Estrategia_detalle,Rol,Centro_de_formacion
from django.http import HttpRequest, HttpResponse, JsonResponse
from apps.core.models import Municipio,Regional,Bilinguismo_programa
from apps.core.forms import Form_meta, Form_meta_formacion, Form_estrategias, Form_meta_estrategia_detalle,Form_modalidad, Form_Bilinguismo_programa, Form_centro_de_formacion,Form_regional,Form_nivel_formacion
from django.views.generic import TemplateView, CreateView, UpdateView
from apps.core.models import Programas_formacion,Nivel_formacion
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,DeleteView
from django.db.models import Count,Sum
from datetime import datetime
from django.urls import reverse_lazy
from .serializers import MetaSerializer,EstrateiaSerializer
from django.utils import timezone
from apps.personas.models import Rol,Persona_rol
from apps.personas.decorators import permission_required
from datetime import datetime, date
from django.contrib import messages
import json
from django.core.paginator import Paginator
#redirecciones a las vistas
def menu(request):
    return render(request,'home.html')

def inicio_sesion(request):
    return render(request,'inicio_sesion.html')

def registro(request):
    return render(request, 'registro.html')

def Verificar_año(request):
    
    if request.method == 'POST':
       
        data = json.loads(request.body)
        met_año = data.get('id_met_año')
       
        existe = Meta.objects.filter(met_año=met_año).exists()
        
        return JsonResponse({'existe':existe})


def estrategias_institucionales(request):
    return render(request, 'Estrategias_institucionales/estrategias_institucionales.html')

def formacion_regular(request):
    return render(request, 'Formacion_regular/formacion_regular.html')

#Graficas de es
def estrategias(request):
    
    #filtros de fecha
    select_fecha_inicio = request.GET.get('fecha_inicio')
    
    select_fecha_fin = request.GET.get('fecha_fin')
    
    datos_p04= P04.objects.all()
    
    
   
    
    if select_fecha_inicio and select_fecha_fin:
        datos_p04 = datos_p04.filter(fecha_inicio_ficha__gte=select_fecha_inicio, fecha_inicio_ficha__lte=select_fecha_fin)
   
    
    
    
    filtro_modalidad_presencial = 'PRESENCIAL'
    filtro_modalidad_virtual = 'VIRTUAL'
    
    data_presencial = datos_p04.filter(modalidad_formacion=filtro_modalidad_presencial)
    data_virtual = datos_p04.filter(modalidad_formacion=filtro_modalidad_virtual)
    data_presencial =  datos_p04.filter(modalidad_formacion=filtro_modalidad_presencial)
    
    
    data_virtual =  datos_p04.filter(modalidad_formacion=filtro_modalidad_virtual)
    
    #DATOS PARA LAS GRAFICAS DEL P04
    
    def calcular_total_aprendices(data_presencial, data_virtual,nivel_formacion):
        total_presencial = sum(aprendices['total_aprendices_activos'] for aprendices in data_presencial.filter(nivel_formacion=nivel_formacion).values('total_aprendices_activos'))
        total_virtual = sum(aprendices['total_aprendices_activos'] for aprendices in data_virtual.filter(nivel_formacion=nivel_formacion).values('total_aprendices_activos'))
        
        return total_presencial, total_virtual
    
    total_curso_especial_activos = calcular_total_aprendices(data_presencial,data_virtual,'CURSO ESPECIAL')
    total_tecnologo_activos = calcular_total_aprendices(data_presencial,data_virtual,'TECNÓLOGO')
    total_tecnico_activos = calcular_total_aprendices(data_presencial,data_virtual,'TÉCNICO')
    total_auxiliar_activos = calcular_total_aprendices(data_presencial,data_virtual,'AUXILIAR')
    total_operario_activos = calcular_total_aprendices(data_presencial,data_virtual,'OPERARIO')
    total_evento_activos = calcular_total_aprendices(data_presencial,data_virtual,'EVENTO')
    total_profundizacion_tecnica_activos = calcular_total_aprendices(data_presencial,data_virtual,'PROFUNDIZACION TECNICA')
    
    #datos para conplementaria  bilinguismo
    def calcular_total_aprendices_complementario(data_presencial, data_virtual,nivel_formacion):
        total_presencial_complementaria = sum(aprendices['total_aprendices_activos'] for aprendices in data_presencial.filter(nombre_programa_especial=nivel_formacion).values('total_aprendices_activos'))
        total_virtual_complementaria= sum(aprendices['total_aprendices_activos'] for aprendices in data_virtual.filter(nombre_programa_especial=nivel_formacion).values('total_aprendices_activos'))
        
        return total_presencial_complementaria, total_virtual_complementaria
    
    total_bilinguismo_activos = calcular_total_aprendices_complementario(data_presencial,data_virtual,'PROGRAMA DE BILINGUISMO')
    
    #datos para complementaria sin bilinguismo
    
    def calcular_total_aprendices_complementario_sin_bilinguismo(data_presencial,data_virtual,nivel_formacion):
        
        sin_bilinguismo_presencial= data_presencial.filter(nivel_formacion=nivel_formacion).values('total_aprendices_activos')
        sin_bilinguismo_virtual= data_virtual.filter(nivel_formacion=nivel_formacion).values('total_aprendices_activos')
        

        total_presencial_sin_bilinguismo = sum(aprendices['total_aprendices_activos'] for aprendices in sin_bilinguismo_presencial.exclude(nombre_programa_especial='PROGRAMA DE BILINGUISMO'))
        total_virtual_sin_bilinguismo = sum(aprendices['total_aprendices_activos'] for aprendices in sin_bilinguismo_virtual.exclude(nombre_programa_especial='PROGRAMA DE BILINGUISMO').values('total_aprendices_activos'))
      
    
        return total_presencial_sin_bilinguismo,total_virtual_sin_bilinguismo

    total_sin_bilinguismo_activos = calcular_total_aprendices_complementario_sin_bilinguismo(data_presencial,data_virtual,'CURSO ESPECIAL')
    
    auxiliar_presencial, auxiliar_virtual = total_auxiliar_activos
    tecnico_presencial, tecnico_virtual = total_tecnico_activos
    tecnologo_presencial, tecnologo_virtual = total_tecnologo_activos
    profundizacion_tecnica_presencial, profundizacion_tecnica_virtual = total_profundizacion_tecnica_activos
    evento_presencial, evento_virtual = total_evento_activos
    operario_presencial, operario_virtual = total_operario_activos
    curso_especial_presencial, curso_especial_virtual = total_curso_especial_activos
    bilinguismo_presencial, bilinguismo_virtual = total_bilinguismo_activos
    sin_bilinguismo_presencial, sin_bilinguismo_virtual = total_sin_bilinguismo_activos
    
    data_presencial_p04_tabla = [auxiliar_presencial,tecnico_presencial,tecnologo_presencial,profundizacion_tecnica_presencial,evento_presencial,operario_presencial,curso_especial_presencial,bilinguismo_presencial,sin_bilinguismo_presencial]
    data_virtual_p04_tabla = [auxiliar_virtual,tecnico_virtual,tecnologo_virtual,profundizacion_tecnica_presencial,evento_virtual,operario_virtual,curso_especial_virtual,bilinguismo_virtual,sin_bilinguismo_virtual]
    
    
    
    #DATOS DE LAS METAS DE ESTRATEGIA 

    select_estrategia = request.GET.get('estrategia')
    
    
    if not select_estrategia:
        estrategia_predeterminada = Estrategia_detalle.objects.first()
        if estrategia_predeterminada:
            # Si hay una estrategia, asignarla a select_estrategia
            select_estrategia = estrategia_predeterminada.est_id
        else:
            # Enviar un mensaje de error si no hay estrategias en la base de datos
            messages.error(request, 'No hay estrategias disponibles en la base de datos.')
            return render(request, 'Estrategias/estrategias.html') 
    try:
        # Comprobar si el ID de la estrategia existe
        Estrategia_detalle.objects.get(est_id=select_estrategia)
    except Estrategia_detalle.DoesNotExist:
        # Enviar un mensaje de error si la estrategia no existe
        messages.error(request, 'La estrategia seleccionada no existe en la base de datos.')
        return redirect('nombre_de_tu_vista')  # Cambia 'nombre_de_tu_vista' por el nombre adecuado

    metas_estrategias = Estrategia_detalle.objects.all()
    if select_estrategia:
        metas_estrategias = Estrategia_detalle.objects.filter(est_id=select_estrategia)
        
    presencial_meta = metas_estrategias.filter(estd_modalidad=1)
    virtual_meta_estrategia = metas_estrategias.filter(estd_modalidad=2)
  
    
    auxiliar = []
    tecnico= []
    tecnologo  =[]
    profundizacion_tecnica = []
    evento = []
    operario = []
    curso_especial = []
    bilinguismo = []
    sin_bilinguismo =[]
        

    #separa las metas para cada nivel de formacion en virtual y presencial
    
    for meta in presencial_meta:
        auxiliar.append(int(meta.estd_auxiliar_meta))
        tecnico.append(int(meta.estd_tecnico_meta))
        tecnologo.append(int(meta.estd_tecnologo))
        profundizacion_tecnica.append(int(meta.estd_profundizacion_tecnica_meta))
        evento.append(int(meta.estd_evento))
        operario.append(int(meta.estd_operario_meta))
        curso_especial.append(int(meta.estd_curso_especial))
        bilinguismo.append(int(meta.estd_bilinguismo))
        sin_bilinguismo.append(int(meta.estd_sin_bilinguismo))
        
    for meta in virtual_meta_estrategia:
        auxiliar.append(int(meta.estd_auxiliar_meta))
        tecnico.append(int(meta.estd_tecnico_meta))
        tecnologo.append(int(meta.estd_tecnologo))
        profundizacion_tecnica.append(int(meta.estd_profundizacion_tecnica_meta))
        evento.append(int(meta.estd_evento))
        operario.append(int(meta.estd_operario_meta))
        curso_especial.append(int(meta.estd_curso_especial))
        bilinguismo.append(int(meta.estd_bilinguismo))
        sin_bilinguismo.append(int(meta.estd_sin_bilinguismo))
        
    
    context = {
        'total_curso_especial_activos':json.dumps(total_curso_especial_activos),
        'total_tecnologo_activos':json.dumps(total_tecnologo_activos),
        'total_tecnico_activos':json.dumps(total_tecnico_activos),
        'total_auxiliar_activos':json.dumps(total_auxiliar_activos),
        'total_operario_activos':json.dumps(total_operario_activos),
        'total_evento_activos':json.dumps(total_evento_activos),
        'total_profundizacion_tecnica_activos':json.dumps(total_profundizacion_tecnica_activos),
        'total_bilinguismo_activos':json.dumps(total_bilinguismo_activos),
        'total_sin_bilinguismo_activos':json.dumps(total_sin_bilinguismo_activos),
        'estrategias':Estrategia.objects.all(),
        'select_estrategia':select_estrategia,
        'presencial_meta':presencial_meta,
        'virtual_meta_estrategia':virtual_meta_estrategia,
        'data_presencial_p04_tabla':data_presencial_p04_tabla,
        'data_virtual_p04_tabla':data_virtual_p04_tabla,
        #METAS PARA PORCENTAJES
        'auxiliar_meta':json.dumps(auxiliar),
        'tecnico_meta':json.dumps(tecnico),
        'tecnologo_meta':json.dumps(tecnologo),
        'profundizacion_tecnica_meta':json.dumps(profundizacion_tecnica),
        'evento_meta':json.dumps(evento),
        'operario_meta':json.dumps(operario),
        'curso_especial_meta':json.dumps(curso_especial),
        'bilinguismo_meta':json.dumps(bilinguismo),
        'sin_bilinguismo_meta':json.dumps(sin_bilinguismo)
    }


    return render(request, 'Estrategias/estrategias.html',context)

from django.db.models import Q
def general(request):
    year = datetime.now().year
    select_fecha_inicio_default = f"{year}-01-01"
    select_fecha_fin_default = f"{year}-12-31"
    #filtros de fecha
    select_fecha_inicio = request.GET.get('fecha_inicio',select_fecha_inicio_default)
    
    select_fecha_fin = request.GET.get('fecha_fin',select_fecha_fin_default)
    select_fecha_fin_ff = datetime.strptime(select_fecha_fin, "%Y-%m-%d").date()
    select_fecha_inicio_ff = datetime.strptime(select_fecha_inicio, "%Y-%m-%d").date()

    datos_p04= P04.objects.all()
    
    
   
    
    if select_fecha_inicio and select_fecha_fin:
        datos_p04 = datos_p04.filter(fecha_inicio_ficha__gte=select_fecha_inicio, fecha_inicio_ficha__lte=select_fecha_fin)
    
     

        
    #funcionalida para grafica titulada
 
    filtro_modalidad_presencial = 'PRESENCIAL'
    filtro_modalidad_virtual = 'VIRTUAL'
    
    data_presencial =  datos_p04.filter(modalidad_formacion=filtro_modalidad_presencial)
    
    
    data_virtual =  datos_p04.filter(modalidad_formacion=filtro_modalidad_virtual)
    
    
    niveles_habilitados = {
        'CURSO ESPECIAL' : 0,
        'TECNÓLOGO' : 0,
        'TÉCNICO' : 0,
        'AUXILIAR' : 0,
        'OPERARIO' : 0,
        'EVENTO' : 0,
    }
    niveles_habilitados_virtual = {
        'CURSO ESPECIAL' : 0,
        'TECNÓLOGO' : 0,
        'TÉCNICO' : 0,
        'AUXILIAR' : 0,
        'OPERARIO' : 0,
        'EVENTO' : 0,
      
    }
    
    #PRESENCIAL
    for aprendiz in data_presencial:
        activos = aprendiz.total_aprendices_activos
        nivel = aprendiz.nivel_formacion
    
        if nivel in niveles_habilitados:
            niveles_habilitados[nivel] += activos
    #VIRTUAL
    for aprendiz in data_virtual:
        activos = aprendiz.total_aprendices_activos
        nivel = aprendiz.nivel_formacion
        
        if nivel in niveles_habilitados_virtual:
            niveles_habilitados_virtual[nivel] += activos
    
    
    
   
    #DATOS PARA RENDERIZAR LAS GRAFICAS 
    labels_presenciales = [f'{nivel} Presencial' for nivel in  niveles_habilitados.keys()] 
    labels_virtuales = [f'{nivel} Virtual' for nivel in  niveles_habilitados_virtual.keys()]
    data_values_presencial = list(niveles_habilitados.values())
    data_values_virtual = list(niveles_habilitados_virtual.values())
    data =data_values_presencial + data_values_virtual
    
    
    #NOTA VERIFICA QUE PRESENCIAL=1,VIRTUAL=2,DISTANCIA=3
    print("Fecha Inicio:", type(select_fecha_fin_ff))
    print("Fecha Fin:", select_fecha_fin_ff)

    modalidad_presencial_metas = 1
    modalidad_virtual_metas = 2
    metas_ids = Meta.objects.filter(
        met_fecha_inicio__lte=select_fecha_fin_ff,
        met_fecha_fin__gte=select_fecha_inicio_ff,

    ).values_list('met_id', flat=True)
    print("IDs de Metas para el rango de fechas:", list(metas_ids))
    
    
  
    #METAS CON PORCENTAJES
    metas_presencial_porcentaje = Metas_formacion.objects.filter(metd_modalidad=modalidad_presencial_metas, met_id__met_fecha_inicio__lte=select_fecha_fin_ff,met_id__met_fecha_fin__gte=select_fecha_inicio_ff) 
   
    metas_virtual_porcentaje = Metas_formacion.objects.filter(metd_modalidad=modalidad_virtual_metas,met_id__met_fecha_inicio__lte=select_fecha_fin_ff, met_id__met_fecha_fin__gte=select_fecha_inicio_ff)
    
    metas_presencial_porcentaje_res = list(metas_presencial_porcentaje.values_list('met_formacion_curso_especial','met_formacion_tecnologo','met_formacion_tecnico','met_formacion_auxiliar','met_formacion_operario','met_formacion_evento'))
    metas_virtual_porcentaje_res = list(metas_virtual_porcentaje.values_list('met_formacion_curso_especial','met_formacion_tecnologo','met_formacion_tecnico','met_formacion_auxiliar','met_formacion_operario','met_formacion_evento'))
    print('kk',metas_presencial_porcentaje_res)
    def sumar_tuplas(metas):
        if len(metas) == 1:
            return [metas[0]]  # Devuelve una lista con la tupla si hay solo una

    # Suma los elementos de las tuplas
        suma = tuple(sum(x) for x in zip(*metas))
        return [suma]  # Devuelve la suma dentro de una lista

    metas_presencial_porcentaje_suma = []  # Inicializa como lista vacía si no hay datos
    metas_virtual_porcentaje_suma = [] 
    metas_presencial_porcentaje_suma = sumar_tuplas(metas_presencial_porcentaje_res)
    metas_virtual_porcentaje_suma = sumar_tuplas(metas_virtual_porcentaje_res)
   
    metas = metas_presencial_porcentaje_suma + metas_virtual_porcentaje_suma
    
    metas_conversion = sum(metas, ())
    metas_valores = list(metas_conversion)
    
    #FUNCIONALIDAD PARA GRAFICA COMPLEMENTARIA
    
    
    #DATOS PARA RENDERIZAR LAS GRAFICAS 
    
    #virtual bilinguismo
    
    bilinguismo = data_virtual.filter(nombre_programa_especial='PROGRAMA DE BILINGUISMO').values('total_aprendices_activos')
    bilinguismo_activos_virtual = [aprendices_bilinguismo['total_aprendices_activos'] for aprendices_bilinguismo in bilinguismo]
    bilinguismo_activos_data_virtual = sum(bilinguismo_activos_virtual)
    
    #presencial bilinguismo
    
    bilinguismo = data_presencial.filter(nombre_programa_especial='PROGRAMA DE BILINGUISMO').values('total_aprendices_activos')
    bilinguismo_activos_presencial = [aprendices_bilinguismo_presencial['total_aprendices_activos'] for aprendices_bilinguismo_presencial in bilinguismo]
    
    bilinguismo_activos_data_presencial = sum(bilinguismo_activos_presencial)
    
    
    
    #virtual sin bilinguismo 
    sin_bilinguismo = data_virtual.filter(nivel_formacion='CURSO ESPECIAL').values('total_aprendices_activos')
    
    sin_bilinguismo_data = sin_bilinguismo.exclude(nombre_programa_especial='PROGRAMA DE BILINGUISMO')
    sin_bilinguismo_activos_virtual = [aprendices_sin_bilinguismo_virtual['total_aprendices_activos'] for aprendices_sin_bilinguismo_virtual in sin_bilinguismo_data]
    
    sin_bilinguismo_activos_data_virtual = sum(sin_bilinguismo_activos_virtual)
    
    
    #presencial sin bilinguismo 
    sin_bilinguismo = data_presencial.filter(nivel_formacion='CURSO ESPECIAL').values('total_aprendices_activos')
    
    sin_bilinguismo_data = sin_bilinguismo.exclude(nombre_programa_especial='PROGRAMA DE BILINGUISMO')
    sin_bilinguismo_activos_presencial = [aprendices_sin_bilinguismo_presencial['total_aprendices_activos'] for aprendices_sin_bilinguismo_presencial in sin_bilinguismo_data]
    
    sin_bilinguismo_activos_data_presencial = sum(sin_bilinguismo_activos_presencial)
    
    
    #funcion para manejar las metas por los diferentes años seleccionados 
    def procesar_metas(metas):
        if len(metas) == 1:
            return [metas[0]] 
        else:
            return [sum(metas)] 
        
    #metas presencial bilinguismo 
    metas_presencial_bilinguismo = Metas_formacion.objects.filter(metd_modalidad=modalidad_presencial_metas, met_id__met_fecha_inicio__lte=select_fecha_fin_ff,met_id__met_fecha_fin__gte=select_fecha_inicio_ff)
    #bilinguismo presencial
    metas_formacion_bilinguismo_presencial = metas_presencial_bilinguismo.values('met_formacion_bilinguismo')
    bilinguismo_meta_presencial = [bilinguismo_metas_presencial['met_formacion_bilinguismo'] for bilinguismo_metas_presencial in metas_formacion_bilinguismo_presencial]
  
    #sin bilinguismo presencial
    metas_formacion_sin_bilinguismo_presencial = metas_presencial_bilinguismo.values('met_formacion_sin_bilinguismo')
    sin_bilinguismo_meta_presencial = [sin_bilinguismo_metas_presencial['met_formacion_sin_bilinguismo'] for sin_bilinguismo_metas_presencial in metas_formacion_sin_bilinguismo_presencial]
    
    #metas presencial sin bilinguismo 
    metas_virtual_bilinguismo = Metas_formacion.objects.filter(metd_modalidad=modalidad_presencial_metas, met_id__met_fecha_inicio__lte=select_fecha_fin_ff,met_id__met_fecha_fin__gte=select_fecha_inicio_ff)
    #bilinguismo virtual
    metas_formacion_bilinguismo_virtual = metas_virtual_bilinguismo.values('met_formacion_bilinguismo')
    bilinguismo_meta_virtual = [bilinguismo_metas_virtual['met_formacion_bilinguismo'] for bilinguismo_metas_virtual in metas_formacion_bilinguismo_virtual]
    #sin bilinguismo virtual
    metas_formacion_sin_bilinguismo_virtual = metas_virtual_bilinguismo.values('met_formacion_sin_bilinguismo')
    sin_bilinguismo_meta_virtual = [sin_bilinguismo_metas_virtual['met_formacion_sin_bilinguismo'] for sin_bilinguismo_metas_virtual in metas_formacion_sin_bilinguismo_virtual]
    
    
    bilinguismo_meta_presencial_suma = procesar_metas(bilinguismo_meta_presencial)
    bilinguismo_meta_virtual_suma = procesar_metas(bilinguismo_meta_virtual)
    sin_bilinguismo_meta_presencial_suma = procesar_metas(sin_bilinguismo_meta_presencial)
    sin_bilinguismo_meta_virtual_suma = procesar_metas(sin_bilinguismo_meta_virtual)
    
  
    
    metas_complementaria = bilinguismo_meta_presencial_suma + bilinguismo_meta_virtual_suma + sin_bilinguismo_meta_presencial_suma + sin_bilinguismo_meta_virtual_suma
  
    aprendices_activos_complementaria= [bilinguismo_activos_data_presencial , bilinguismo_activos_data_virtual , sin_bilinguismo_activos_data_presencial , sin_bilinguismo_activos_data_virtual]
    
     
    

    context = {
        #grafica titulada
        'labels_presenciales':json.dumps(labels_presenciales),
        'labels_virtuales':json.dumps(labels_virtuales),
        'data':data,
  
       
        'data_tabla_presencial':data_values_presencial,
        'data_tabla_virtual':data_values_virtual,
     
        'metas_valores':json.dumps(metas_valores),
        'select_fecha_fin':select_fecha_fin,
        'select_fecha_inicio':select_fecha_inicio,
        #grafica complementaria
        'bilinguismo_activos_virtual':bilinguismo_activos_data_virtual,
        'bilinguismo_activos_data_presencial':bilinguismo_activos_data_presencial,
        
        'sin_bilinguismo_activos_data_virtual':sin_bilinguismo_activos_data_virtual,
        'sin_bilinguismo_activos_data_presencial':sin_bilinguismo_activos_data_presencial,
        #metas tabla
        'metas_presencial':metas_presencial_porcentaje_suma,
        'metas_virtual':metas_virtual_porcentaje_suma,
        'metas_formacion_bilinguismo_virtual':metas_formacion_bilinguismo_virtual,
        #metas complementaria tablas
        'metas_formacion_bilinguismo_presencial':bilinguismo_meta_presencial_suma,
        'metas_formacion_sin_bilinguismo_presencial':sin_bilinguismo_meta_presencial_suma,
        'metas_formacion_bilinguismo_virtual':bilinguismo_meta_virtual_suma,
        'metas_formacion_sin_bilinguismo_virtual':sin_bilinguismo_meta_virtual_suma,
      
        #metas_complementaria
        'metas_complementaria':metas_complementaria,
        'aprendices_activos_complementaria':aprendices_activos_complementaria,
      
    }



    return render(request, 'General/general.html', context)








def grafica(request):
    return render(request, 'Estrategias/grafica.html')



@permission_required('can_view_admin_dashboard')
def administrador(request):
    personas = Persona.objects.all()
    roles = Rol.objects.all()

    return render(request, 'administrador.html', {'personas': personas, 'roles':roles})




#FUNCIONALIDADES

#COBERTURA

def cobertura(request):
    municipio = Municipio.nombre.field.choices
    centro_de_formacion= Centro_de_formacion.objects.all(),
 
    context = {
        'centro_de_formacion':centro_de_formacion,
        'municipio':municipio
    }
    return render(request, 'Cobertura/cobertura.html', context)
from collections import Counter
class Cobertura_mapa(TemplateView):
    template_name = 'Cobertura/cobertura.html'
    
    def get(self, request, *args, **kwargs):
        selected_municipio = request.GET.get('nombre_municipio', '')
        selected_fecha_inicio = request.GET.get('filtroFechaInicio')
        selected_fecha_fin = request.GET.get('filtroFechaFin')
        selected_centro_de_formacion = request.GET.get('id_centro_de_formacion')
        print('id',selected_centro_de_formacion)
        
        
        municipio = Municipio.nombre.field.choices

    
        if not selected_fecha_fin:
            selected_fecha_fin = timezone.now().date()
            
    
        p04 = P04.objects.all()
        
        if selected_fecha_inicio and selected_fecha_fin:
            p04 = p04.filter(fecha_inicio_ficha__range=[selected_fecha_inicio, selected_fecha_fin])
        elif selected_fecha_inicio:
            p04 = p04.filter(fecha_inicio_ficha__gte=selected_fecha_inicio)


        if selected_municipio:
            p04 = p04.filter(nombre_municipio_curso=selected_municipio)
        if selected_centro_de_formacion:
            def seleccionar_nombre_centro(id_centro):
                nombre_centro = get_object_or_404(Centro_de_formacion, id=id_centro)
                
                return nombre_centro.centro_de_formacion
            centro_de_formacion_res = seleccionar_nombre_centro(selected_centro_de_formacion)
            
            p04 = p04.filter(nombre_centro=centro_de_formacion_res)
            print(p04)
        elif selected_centro_de_formacion and selected_municipio:
            def seleccionar_nombre_centro(id_centro):
                nombre_centro = get_object_or_404(Centro_de_formacion, id=id_centro)
                
                return nombre_centro.centro_de_formacion
            centro_de_formacion_res = seleccionar_nombre_centro(selected_centro_de_formacion)
            
            p04 = p04.filter(nombre_centro=centro_de_formacion_res,nombre_municipio_curso=selected_municipio)
            print(p04)
        programas_lista = list(p04.values_list('nombre_programa_formacion','nivel_formacion'))
        programas_conteo = Counter(programas_lista)
        
        programa_data = [{'programa': programa,'nivel_formacion':nivel_formacion, 'programa_count': count} for (programa,nivel_formacion), count in programas_conteo.items()]
    
        context = self.get_context_data(
            programa_data=programa_data,
            centro_de_formacion= Centro_de_formacion.objects.all(),
            municipio=municipio,
            selected_municipio=selected_municipio,
            selected_fecha_inicio=selected_fecha_inicio,
            selected_fecha_fin=selected_fecha_fin,
            programas_conteo=programas_conteo,
            
            selected_centro_de_formacion=selected_centro_de_formacion
            
            )
        return self.render_to_response(context)



#PROGRAMA
def capitalizar_texto(text):
    return text.capitalize()
def Programa_index(request):
    modalidad = Modalidad.objects.all()
    programa_formacion_choices = Programas_formacion.Programas_formacion_choices.choices
    nivel_formacion = Nivel_formacion.Nivel_formacion_choices.choices
    context = {
        'modalidad': modalidad,
        'programa_formacion': programa_formacion_choices,
        'nivel_formacion':nivel_formacion,
       
        
       
    }
    return render(request, 'Programa/programa.html', context)

class Programa(TemplateView):
    template_name = 'Programa/programa.html'
    
    def get(self, request, *args, **kwargs):
        selected_centro_de_formacion = request.GET.get('centro_de_formacion','')
        selected_nivel_formacion = request.GET.get('nivel_formacion','')
        selected_programa_formacion = request.GET.get('programa_formacion','')
        print('pppp',selected_nivel_formacion)
        selected_modalidad = request.GET.get('modalidad','')
        
        

        modalidad_nombre = ''
        id_modalidad = None
        if selected_modalidad == '1':
            
            modalidad_nombre = 'PRESENCIAL'
            
            id_modalidad = 1
        elif selected_modalidad == '2':
            id_modalidad = 2
            modalidad_nombre = 'VIRTUAL'
            
            
        selected_modalidades = [{'id':id_modalidad,'modalidad':capitalizar_texto(modalidad_nombre)}]
        
        
        
    
        modalidad_id = {
            'PRESENCIAL':1,
            'VIRTUAL':2,
            'A DISTANCIA':3,
            
        }
        modalidades_habilitados = P04.objects.filter(nombre_programa_formacion=selected_programa_formacion).values('modalidad_formacion').distinct()
        valores_modalidad = [
          {
        'id': modalidad_id.get(modalidad['modalidad_formacion'].upper(), 0),  # Obtener el ID
        'modalidad': capitalizar_texto(modalidad['modalidad_formacion'])  # Capitalizar el nombre
        } for modalidad in modalidades_habilitados ]
     
  
        
        
            
        #FILTROS DE PROGRAMA
        
        filtros_programa = {}
        
        valores_programa = []
        
        
        centro_de_formacion_res  = None
        nivel_formacion_res = None
        
        if selected_centro_de_formacion:
            def obtener_nombre_centro_formacion(id_centro_formacion):
                nombre_centro_formacion= get_object_or_404(Centro_de_formacion, id=id_centro_formacion)
                print('nombre_centro_formacion',nombre_centro_formacion)
                return nombre_centro_formacion.centro_de_formacion
        
            centro_de_formacion_res = obtener_nombre_centro_formacion(selected_centro_de_formacion)
            filtros_programa['nombre_centro'] = centro_de_formacion_res
        
            
        if selected_nivel_formacion:
            
            def obtener_nombre_nivel_formacion(id_nivel_formacion):
                nombre_nivel_formacion = get_object_or_404(Nivel_formacion, id=id_nivel_formacion)
                return nombre_nivel_formacion.nivel_formacion
        
            nivel_formacion_res = obtener_nombre_nivel_formacion(selected_nivel_formacion)
           
        
            if nivel_formacion_res == 'BILINGUISMO':
                filtros_programa['nombre_programa_especial'] = 'PROGRAMA DE BILINGUISMO'
                
                programas_bilinguismo = Bilinguismo_programa.objects.all().values_list('Bil_programa', flat=True)
       
            
                programas_habilitados = P04.objects.filter(nivel_formacion='CURSO ESPECIAL', nombre_programa_formacion__in=programas_bilinguismo).values('nombre_programa_formacion').distinct()
             
                valores_programa = [programa['nombre_programa_formacion']for programa in programas_habilitados]
            
            elif nivel_formacion_res == 'SIN BILINGUISMO':

                programas_bilinguismo = Bilinguismo_programa.objects.all().values_list('Bil_programa', flat=True)
                lista_filtros = P04.objects.filter(**filtros_programa).exclude(nombre_programa_formacion__in=programas_bilinguismo)

                programas_sin_bilinguismo = P04.objects.all().values_list('nombre_programa_formacion', flat=True).exclude(nombre_programa_formacion__in=programas_bilinguismo)
                
                valores_programa = programas_sin_bilinguismo
             

                filtros_programa['nivel_formacion'] = 'CURSO ESPECIAL'
               
            else:
                filtros_programa['nivel_formacion'] = nivel_formacion_res
                programas_habilitados = P04.objects.filter(nivel_formacion=nivel_formacion_res,nombre_centro=centro_de_formacion_res).values('nombre_programa_formacion').distinct()
               
                valores_programa = [programa['nombre_programa_formacion']for programa in programas_habilitados]
                
        
                
        if selected_programa_formacion:
         
            filtros_programa['nombre_programa_formacion'] = selected_programa_formacion
          
        if selected_modalidad:
            if selected_modalidad == '1':
                selected_modalidad = 'PRESENCIAL'
            elif selected_modalidad == '2':
                selected_modalidad = 'VIRTUAL'  
            elif selected_modalidad == '3':
                selected_modalidad = 'A DISTANCIA' 
            filtros_programa['modalidad_formacion'] = selected_modalidad
       
        
        
            
        
        lista_filtros = P04.objects.filter(**filtros_programa)
       
        
        municipios_filtro = lista_filtros.values('nombre_municipio_curso').annotate(programa_count=Count('nombre_programa_formacion')).order_by('nombre_municipio_curso')
        paginator1 = Paginator(municipios_filtro,10)
        page_number1 = request.GET.get('page1')
        page_obj1 = paginator1.get_page(page_number1)
        
        fichas_filtro = lista_filtros.values('identificador_ficha').order_by('identificador_ficha')
        paginator2 = Paginator(fichas_filtro,10)
        page_number2 = request.GET.get('page2')
        page_obj2 = paginator2.get_page(page_number2)
 
     
        context = self.get_context_data(
            nivel_formacion=Nivel_formacion.objects.all(),
            centro_de_formacion= Centro_de_formacion.objects.all(),
            programa_formacion=valores_programa,
            modalidad=valores_modalidad,
            
            #Mantiene la opcion en el select
            selected_nivel_formacion=selected_nivel_formacion,
            selected_programa_formacion=selected_programa_formacion,
            selected_modalidad=selected_modalidades,
            selected_centro_de_formacion=selected_centro_de_formacion,
            
            lista_municipios=page_obj1,
            lista_fichas = page_obj2,
           
          
            
        )
      
            
        return self.render_to_response(context)


#detalle de la ficha seleccionada
def detalle_ficha(request, identificador_ficha):
   
    ficha = get_object_or_404(P04, identificador_ficha=identificador_ficha)
    data = {
        'identificador_ficha': ficha.identificador_ficha,
        'campo1': ficha.modalidad_formacion,
        'campo2': ficha.nombre_centro,
        'campo3': ficha.tipo_de_formacion,
        'campo4': ficha.fecha_inicio_ficha,
        'campo5': ficha.fecha_terminacion_ficha,
        'campo6': ficha.red,
        'campo7': ficha.nombre_municipio_curso,
        'campo8': ficha.nombre_programa_formacion,
        'campo9': ficha.nivel_formacion,
        
    }
   
    return JsonResponse(data)




class Desercion(TemplateView):
    template_name = 'Desercion/desercion.html'
    
    
    def get(self, request, *args, **kwargs):
        
        
       
        
        select_modalidad = request.GET.get('id_modalidad','')
        select_municipio = request.GET.get('municipio','')
        select_regional = request.GET.get('regional', '')
        select_centro_de_formacion = request.GET.get('centro_de_formacion','')
        select_fecha_inicio_ficha = request.GET.get('fecha_inicio_ficha')
        select_fecha_terminacion_ficha = request.GET.get('fecha_terminacion_ficha')
      
        
        
       
       
       
        filtros_desercion = {}
        

        if select_fecha_inicio_ficha:
        # Convertir la fecha de inicio a formato de fecha y aplicar filtro mayor o igual
            fecha_inicio = datetime.strptime(select_fecha_inicio_ficha, '%Y-%m-%d').date()
            filtros_desercion['fecha_inicio_ficha__gte'] = fecha_inicio
        else:
            # Si no se proporciona fecha de inicio, asignar por defecto
            fecha_inicio = date(date.today().year, 1, 1)
            select_fecha_inicio_ficha = fecha_inicio.strftime('%Y-%m-%d')
            filtros_desercion['fecha_inicio_ficha__gte'] = fecha_inicio
        # Si se proporciona fecha de terminación, convertirla a formato de fecha y aplicar filtro menor o igual
        if select_fecha_terminacion_ficha:
            fecha_fin = datetime.strptime(select_fecha_terminacion_ficha, '%Y-%m-%d').date()
            filtros_desercion['fecha_inicio_ficha__lte'] = fecha_fin
        else:
            # Si no se proporciona fecha de terminación, establecerla como la fecha actual
            fecha_fin = date(date.today().year, 12, 31)
            select_fecha_terminacion_ficha = fecha_fin.strftime('%Y-%m-%d')
            filtros_desercion['fecha_inicio_ficha__lte'] = fecha_fin
        modalidades = {
            '1':'PRESENCIAL',
            '2':'VIRTUAL',
            '3':'DISTANCIA'
        }
        if select_modalidad:
            modalidad = modalidades.get(select_modalidad)
            
            
            filtros_desercion['modalidad_formacion'] = modalidad
        
        
        
        
        
        if select_regional:
            def obtener_nombre_regional(id_regional):
                nombre_regional = get_object_or_404(Regional, id=id_regional)
            
                return nombre_regional.regional
            
            regional_res = obtener_nombre_regional(select_regional)
            
            filtros_desercion['nombre_regional'] = regional_res
        if select_centro_de_formacion:
            def obtener_nombre_centro_de_formacion(id_centro):
                
                nombre_centro_formacion = get_object_or_404(Centro_de_formacion, id=id_centro)
                
                return nombre_centro_formacion.centro_de_formacion
            
            centro_de_formacion_res = obtener_nombre_centro_de_formacion(select_centro_de_formacion)
            
            filtros_desercion['nombre_centro'] =centro_de_formacion_res;
            
        if select_municipio:
      
            filtros_desercion['nombre_municipio_curso'] = select_municipio
        
        desercion_datos = P04.objects.filter(**filtros_desercion)
       
        #deserciones
        aprendices_activos_resultado = [resultado.total_aprendices_activos for resultado in desercion_datos]
        aprendices_totales_resultado = [resultado_total.total_aprendices for resultado_total in desercion_datos]

        
        resultado_activo = sum(aprendices_activos_resultado)
       
        
        resultado_total_aprendices = sum(aprendices_totales_resultado)
      
        deserciones = resultado_total_aprendices - resultado_activo
        
        paginator = Paginator(desercion_datos, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = self.get_context_data(
            
            modalidad = Modalidad.objects.all(),
            municipio = Municipio.Municipio_choices.choices,
            regional = Regional.objects.all(),
            centro_de_formacion = Centro_de_formacion.objects.all(),
            
            page_obj=page_obj,
            #mantiene la opcion 
            select_modalidad= select_modalidad,
 
            select_municipio=select_municipio,
            select_regional=select_regional,
            select_centro_de_formacion = select_centro_de_formacion,
            select_fecha_inicio_ficha =select_fecha_inicio_ficha,
            select_fecha_terminacion_ficha =select_fecha_terminacion_ficha,
            
            desercion_datos = desercion_datos,
            aprendices_activos=resultado_activo,
            deserciones=deserciones,
            fecha_actual = date.today().strftime('%Y-%m-%d')
           
        )
        
        return self.render_to_response(context) 

#FORMACION REGULAR 

def Formacion_regular_index(request):
    form = Form_meta
    form_meta_formacion = Form_meta_formacion

 
    context = {
        'form':form,
        'form_meta_formacion' : form_meta_formacion,

        
    }
    return render(request, 'Formacion_regular/formacion_regular.html', context)


class Meta_create(CreateView):
    model = Meta
    form_class = Form_meta
    template_name = 'Formacion_regular/formacion_regular.html'
    success_url = reverse_lazy('cores:formacion_regular_index') 
    
   
    def form_valid(self, form):
        user = self.request.user
        persona = Persona.objects.get(per_documento=user.per_documento)
  
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            metas = Meta.objects.all()
            meta_options = [{'met_id': meta.met_id} for meta in metas]
            return JsonResponse({'success': True, 'options': meta_options,'message': 'Guardado exitosamente'})
        else:
            return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
           
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
        
class meta_delete(DeleteView):

    model = Meta
    success_url = reverse_lazy('cores:meta_index')

def get_meta(request, meta_id):
    try:
        meta = Meta.objects.get(met_id=meta_id)
        data = {
            'meta_id': meta.met_id,
            'met_año': meta.met_año,  # Asegúrate de ajustar estos campos a los que realmente usas
            # Agrega aquí otros campos que necesites
        }
        return JsonResponse(data)
    except Meta.DoesNotExist:
        return JsonResponse({'error': 'Meta no encontrada'}, status=404)
def meta_index(request):
    view_meta = Meta.objects.all()
    form_meta  = Form_meta
  
    
    context = {
         'view_metas':view_meta,
         'form_meta':form_meta
 
    }
    
    return render(request, 'Metas/meta.html',context)

class meta_edit(UpdateView):
    model = Meta
    from_class = Form_meta
    fields = [
        'met_centro_formacion',
        'met_codigo',
        'met_fecha_inicio',
        'met_fecha_fin',
        'met_año',
        'met_total_otras_poblaciones',
        'met_total_victimas',
        'met_total_hechos_victimizantes',
        'met_total_desplazados_violencia',
        'met_total_titulada',
        'met_total_complementaria',
        'met_total_poblacion_vulnerable',

              ]
   
    success_url = reverse_lazy('cores:meta_index')
    
#meta formacion

class Meta_formacion_create(CreateView):
    model = Metas_formacion
    form_class = Form_meta_formacion
    template_name = 'Formacion_regular/formacion_regular.html'
    success_url = reverse_lazy('cores:formacion_regular_index') 

def Verificacion_meta_formacion_regular(request):
    meta_id = request.GET.get('id_met_id')
    
   
    
    modalidades_registrada = Metas_formacion.objects.filter(met_id=meta_id).values('metd_modalidad')
   
    modalidades = Modalidad.objects.filter()
    modalidad_habilitada = Modalidad.objects.exclude(id__in=modalidades_registrada)
   
    opciones_disponibles = [{'id': modalidad.id, 'modalidad':modalidad.modalidad} for modalidad in modalidad_habilitada]
    
    return JsonResponse(opciones_disponibles, safe=False)

class Meta_formacion_delete(DeleteView):
    model = Metas_formacion
    success_url = reverse_lazy('cores:formacion_regular_index')


class Meta_formacion_edit(UpdateView):
    model = Metas_formacion
    from_class = Form_meta_formacion
    fields = ['metd_id',
              'metd_modalidad',
              'met_formacion_operario',
              'met_formacion_auxiliar',
              'met_formacion_tecnico',
              'met_formacion_profundizacion_tecnica',
              'met_formacion_tecnologo',
              'met_formacion_evento',
              'met_formacion_curso_especial',
              'met_formacion_bilinguismo',
              'met_formacion_sin_bilinguismo',
              'met_formacion_sin_bilinguismo',
              'met_id']
    success_url = reverse_lazy('cores:formacion_regular_index')
    
#ESTRATEGIAS_INSTITUCIONALES
def Estrategias_institucionales_index(request):
    form_estrategias_institucionales  = Form_estrategias
    form_meta = Form_meta
    form_meta_estrategia_detalle = Form_meta_estrategia_detalle
    municipio = Municipio.Municipio_choices.choices
    modalidad = Modalidad.objects.all()
    estrategia =    Estrategia.objects.all()
    meta_estrategia =   Estrategia_detalle.objects.all()

  

    
    

    context = {
        'form_estrategias_institucionales':form_estrategias_institucionales,
        'form_meta':form_meta,
        'form_meta_estrategia_detalle': form_meta_estrategia_detalle,
        'municipio':municipio,
        'modalidad':modalidad,
        'estrategia':estrategia,
        'detalle_estrategia':meta_estrategia,



    }
    
    return render(request, 'Estrategias_institucionales/estrategias_institucionales.html', context)
#cruds de  estrategia
class Estrategias_create(CreateView):
    model = Estrategia
    form_class = Form_estrategias
    template_name = 'Estrategias_institucionales/estrategias_institucionales'
    success_url = reverse_lazy('cores:estrategias_institucionales_index')

class estrategia_institucional_delete(DeleteView):
    model = Estrategia
    success_url = reverse_lazy('cores:estrategias_institucionales_index')

class estrategia_institucional_edit(UpdateView):
    model = Estrategia
    from_class = Form_meta_estrategia_detalle
    fields = ['est_nombre','met_id','est_total_meta']
    success_url = reverse_lazy('cores:estrategias_institucionales_index')
    
#meta estrategias intitucionales
class meta_estrategias_intitucionales_delete(DeleteView):
    model = Estrategia_detalle
    success_url = reverse_lazy('cores:estrategias_institucionales_index')


class meta_estrategias_intitucionales_edit(UpdateView):
    model = Estrategia_detalle
    from_class = Form_meta_estrategia_detalle
    fields = ['est_id','estd_modalidad','estd_operario_meta','estd_auxiliar_meta','estd_tecnico_meta','estd_profundizacion_tecnica_meta','estd_tecnologo','estd_evento','estd_curso_especial','estd_bilinguismo','estd_sin_bilinguismo','estd_meta']
    success_url = reverse_lazy('cores:estrategias_institucionales_index')
    
def get_meta_valores(request,met_id):
    
    
    try:
        meta = get_object_or_404(Meta, met_id=met_id)
        data = {
            'met_total_otras_poblaciones': meta.met_total_otras_poblaciones,
            'met_total_victimas' : meta.met_total_victimas,
            'met_total_hechos_victimizantes' : meta.met_total_hechos_victimizantes,
            'met_total_desplazados_violencia' :meta.met_total_desplazados_violencia,
            'met_total_titulada': meta.met_total_titulada,
            'met_total_complementaria': meta.met_total_complementaria,
            'met_total_poblacion_vulnerable': meta.met_total_poblacion_vulnerable,
            
            
   
        
        }
        
        

    
        return JsonResponse(data)
    except Meta.DoesNotExist:
        return JsonResponse({'error': 'Meta not found'},  status=404)


#funciones de meta estrategia, vista estrategias institucionales
from django.http import HttpResponseRedirect
#crear meta estrategia detalle
class Meta_estrategia_detalle(CreateView):
    model = Estrategia_detalle
    form_class = Form_meta_estrategia_detalle
    template_name = 'Estrategias_institucionales/estrategias_institucionales.html'
    success_url = reverse_lazy('cores:estrategias_institucionales_index')
    
    
    #recibe los datos seleccionados
    def post(self, request, *args, **kwargs):
        
        
        
        form = self.get_form()
        print('Contenido del POST:', request.POST)
        
        

        est_id = request.POST.get('est_id')
        estd_meta = request.POST.get('estd_meta')
   
        
        meta_id = int(estd_meta)
       
        

        
       
        form.fields['est_id'].queryset = Estrategia.objects.filter(est_id=est_id)
        form.fields['estd_meta'].initial = meta_id 
     

        if form.is_valid():
               return self.form_valid(form)
        else:
            print('errr', form.errors)
            return self.form_invalid(form)
        

 

   
     

     

#filtros de estrategias 
def get_estrategia_data(request,id_estd_modalidad):

        estrategia = Estrategia.objects.filter(est_modalidad=id_estd_modalidad)


        data = {
        'estrategia': [
            {
                'estrategia_id': e.est_id,
                'estrategia_nombre': e.est_nombre,
            } for e in estrategia
        ]
       }
        
        return JsonResponse(data)
    
#datos para los filtros de meta_estrategia
def meta_data(request,id_estd_meta):
  
    meta = Estrategia.objects.get(met_id=id_estd_meta)
    

    meta_serializer = MetaSerializer(meta)
    
    data = {
        'meta': meta_serializer.data
    }
    return JsonResponse(data)
    
#detalle meta estrategias institucionales

def meta_detalle(request, estd_meta):
    try:
        meta = Meta.objects.get(met_id=estd_meta)
        data = {
            'met_codigo': meta.met_codigo,
            'met_centro_formacion' :meta.met_centro_formacion.centro_de_formacion,
            'met_fecha_inicio' : meta.met_fecha_inicio,
            'met_fecha_fin': meta.met_fecha_fin,
            'met_año' : meta.met_año,
            
        }
      
        return JsonResponse(data)
    except Meta.DoesNotExist:
        return JsonResponse({'Error':'Meta not found'}, status=404)
    

#filtros para gestion formacion



class metas_formacion_filtros(TemplateView):
    model = Metas_formacion
    template_name = 'Formacion_regular/formacion_regular.html'

    def get(self, request, *args, **kwargs):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        modalidad = request.GET.get('modalidad')
        ano = request.GET.get('ano')

        filtros_formacion = {}

        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                filtros_formacion['met_id__met_fecha_fin__gte'] = fecha_inicio
            except ValueError:
                return JsonResponse({'error': 'Fecha de inicio inválida'}, status=400)

        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
                filtros_formacion['met_id__met_fecha_inicio__lte'] = fecha_fin
            except ValueError:
                return JsonResponse({'error': 'Fecha de fin inválida'}, status=400)

        if modalidad:
            filtros_formacion['metd_modalidad'] = modalidad

        if ano:
            filtros_formacion['met_id__met_año'] = ano

        if fecha_inicio or fecha_fin:
            modalidades = Metas_formacion.objects.filter(**filtros_formacion).values_list('metd_modalidad', 'metd_modalidad__modalidad').distinct()
        else:
            modalidades = Modalidad.objects.all().values_list('id', 'modalidad')        

        # Filtrar datos según los filtros aplicados
        resultados = Metas_formacion.objects.filter(**filtros_formacion).values(
            'metd_modalidad__modalidad',
            'metd_modalidad',
            'met_formacion_operario',
            'met_formacion_auxiliar',
            'met_formacion_tecnico',
            'met_formacion_profundizacion_tecnica',
            'met_formacion_tecnologo',
            'met_formacion_evento',
            'met_formacion_curso_especial',
            'met_formacion_bilinguismo',
            'met_formacion_sin_bilinguismo',
            'met_id__met_codigo',
            'met_id__met_centro_formacion',
            'met_id__met_fecha_inicio',
            'met_id__met_fecha_fin',
            'met_id__met_año',
            'met_id',
            'metd_id',
        )

        data = {
            'modalidades': list(modalidades),
            'data': list(resultados)
        }
        return JsonResponse(data)

class estrategias_institucionales_filtros(TemplateView):
    model = Estrategia_detalle
    template_name = 'Estrategias_institucionales/estrategias_institucionales.html'

    def get(self, request, *args, **kwargs):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        modalidad = request.GET.get('modalidad')
        año = request.GET.get('año')
        

        estrategia_detalle_filtro = {}
        

        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            
        if fecha_inicio and fecha_fin:
            id_meta_filtrados = Meta.objects.filter(met_fecha_inicio__gte=fecha_inicio, met_fecha_fin__lte=fecha_fin).values_list('met_id', flat=True)
        elif fecha_inicio:
            id_meta_filtrados = Meta.objects.filter(met_fecha_inicio__gte=fecha_inicio).values_list('met_id',flat=True)
    
        elif fecha_fin:
            id_meta_filtrados = Meta.objects.filter(met_fecha_fin__lte=fecha_fin).values_list('met_id',flat=True)
        
        else:
            id_meta_filtrados = []
     
        if id_meta_filtrados:
               estrategia_detalle_filtro['estd_meta__in'] = id_meta_filtrados
               
              
       
            
        
        if fecha_inicio or fecha_fin:
            modalidades = Estrategia_detalle.objects.filter(**estrategia_detalle_filtro).values_list('estd_modalidad', 'estd_modalidad').distinct()
 
        else:
            modalidades = Modalidad.objects.all().values_list('id', 'modalidad')        
        if modalidad:
            estrategia_detalle_filtro['estd_modalidad'] = modalidad
            
        if año:
            id_metas_año = Meta.objects.filter(met_año=año).values_list('met_id', flat=True)
            estrategia_detalle_filtro['estd_meta__in'] = id_metas_año
            
        
       

            
   

 

        # Filtrar datos según los filtros aplicados
        resultados = Estrategia_detalle.objects.filter(**estrategia_detalle_filtro).values(
            'estd_id',
            'estd_modalidad__modalidad',
            'estd_modalidad',
            'est_id__est_nombre',
            'est_id',
            'estd_operario_meta',
            'estd_auxiliar_meta',
            'estd_tecnico_meta',
            'estd_profundizacion_tecnica_meta',
            'estd_tecnologo',
            'estd_tecnico_meta',
            'estd_evento',
            'estd_curso_especial',
            'estd_bilinguismo',
            'estd_sin_bilinguismo',
            'estd_meta',
           
        )
        

        
       
        

        data = {
            'modalidades': list(modalidades),
            'data': list(resultados)
        }
        return JsonResponse(data)
#CRUD MODALIDAD

def Modalidad_index(request):
    view_modalidades = Modalidad.objects.all()
    form_modalidad = Form_modalidad
    
    context = {
         'view_modalidades':view_modalidades,
         'form_modalidad':form_modalidad,
    }
    
    return render(request, 'Modalidad/modalidad_list.html',context)
class Modalidad_create(CreateView):
    model =  Modalidad
    form_class = Form_modalidad
    template_name = 'Modalidad/modalidad_index.html'
    success_url = reverse_lazy('cores:modalidad_index')

class Modalidad_delete(DeleteView):
    model = Modalidad
    success_url = reverse_lazy('cores:modalidad_index')

class Modalidad_edit(UpdateView):
    model = Modalidad
    from_class = Form_modalidad
    fields = ['modalidad']
    success_url = reverse_lazy('cores:modalidad_index')
    
#CRUD DE BILINGUISMO PROGRAMAS
def Bilinguismo_index(request):
    bilinguismo =  Bilinguismo_programa.objects.all()
   
    form_bilinguismo =  Form_Bilinguismo_programa
    context = {
        'bilinguismo':bilinguismo,
        'form_bilinguismo':form_bilinguismo
    }
    return render(request, 'Bilinguismo/bilinguismo.html', context)

class Bilinguismo_edit(UpdateView):
    model = Bilinguismo_programa
    from_class =  Form_Bilinguismo_programa
   
    fields = ['bil_version','bil_modalidad','Bil_programa','bil_duracion']

    success_url = reverse_lazy('cores:bilinguismo_index')
 
    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
    
class Bilinguismo_create(CreateView):
    model = Bilinguismo_programa
    form_class =  Form_Bilinguismo_programa
    template_name = 'Bilinguismo/bilinguismo.html'
    success_url = reverse_lazy('cores:bilinguismo_index')
    
class Bilinguismo_delete(DeleteView):
    model = Bilinguismo_programa
    success_url = reverse_lazy('cores:bilinguismo_index')
    
    
#CRUD DE CENTRO DE FORMACION
def Centro_de_formacion_index(request):
    centro_de_formacion = Centro_de_formacion.objects.all()
    form_centro_de_formacion = Form_centro_de_formacion
    
    context = {
        'centro_de_formacion':centro_de_formacion,
        'form_centro_de_formacion':form_centro_de_formacion
    }
    return render(request, 'Centro_de_formacion/centro_de_formacion.html', context)

class Centro_de_formacion_create(CreateView):
    model = Centro_de_formacion
    form_class = Form_centro_de_formacion
    template_name = 'Centro_de_formacion/centro_de_formacion.html'
    success_url = reverse_lazy('cores:centro_de_formacion_index')
class Centro_de_formacion_delete(DeleteView):
    model = Centro_de_formacion
    success_url = reverse_lazy('cores:centro_de_formacion_index')
    
class Centro_de_formacion_edit(UpdateView):
    model = Centro_de_formacion
    from_class =Form_centro_de_formacion
    fields = [
        'centro_de_formacion'
    ]
    success_url = reverse_lazy('cores:centro_de_formacion_index')
    

#CRUD DE Regional
def Regional_index(request):
    regional = Regional.objects.all()
    form_regional = Form_regional
    
    context = {
        'regional':regional,
        'form_regional':form_regional
    }
    return render(request, 'Regional/regional.html', context)

class Regional_create(CreateView):
    model = Regional
    form_class = Form_regional
    template_name = 'Regional/regional.html'
    success_url = reverse_lazy('cores:regional_index')
class Regional_delete(DeleteView):
    model = Regional
    success_url = reverse_lazy('cores:regional_index')
    
class Regional_edit(UpdateView):
    model = Regional
    from_class =Form_regional
    fields = [
        'regional'
    ]
    success_url = reverse_lazy('cores:regional_index')
    

#CRUD DE NIVEL FORMAICON
def Nivel_formacion_index(request):
    nivel_formacion = Nivel_formacion.objects.all()
    form_nivel_formacion = Form_nivel_formacion
    
    context = {
        'nivel_formacion':nivel_formacion,
        'form_nivel_formacion':form_nivel_formacion
    }
    return render(request, 'Nivel_formacion/nivel_formacion.html', context)

class Nivel_formacion_create(CreateView):
    model = Nivel_formacion
    form_class = Form_nivel_formacion
    template_name = 'Nivel_formacion/nivel_formacion.html'
    success_url = reverse_lazy('cores:nivel_formacion_index')
class Nivel_formacion_delete(DeleteView):
    model = Nivel_formacion
    success_url = reverse_lazy('cores:nivel_formacion_index')
    
class Nivel_formacion_edit(UpdateView):
    model = Nivel_formacion
    from_class =Form_nivel_formacion
    fields = [
        'nivel_formacion'
    ]
    success_url = reverse_lazy('cores:nivel_formacion_index')
    
     
    


#ROLES

def Asignacion_roles(request):
    if request.method == 'POST':
        persona_id = request.POST.get('persona_id')
        rol_id = request.POST.get('rol_id')

        persona = get_object_or_404(Persona, per_documento=persona_id)
        nuevo_rol = get_object_or_404(Rol, rol_id=rol_id)

        # Elimina todos los roles actuales de la persona
        Persona_rol.objects.filter(persona_id=persona).delete()

        # Asigna el nuevo rol a la persona
        Persona_rol.objects.create(persona_id=persona, rol_id=nuevo_rol, rolp_fecha_inicio=timezone.now(),rolp_fecha_fin=timezone.now())

        return redirect('administrador')
    else:
        return redirect('administrador') 