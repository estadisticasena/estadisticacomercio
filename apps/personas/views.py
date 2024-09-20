from django.forms import BaseModelForm
from django.shortcuts import render
from apps.personas.forms import PersonaForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from apps.personas.models import Persona,Documento_vulnerables_tipo_poblaciones,Documento_vulnerables_poblaciones,Formacion_profesional_integral,Rol,Persona_rol,Programa
from apps.personas.forms import EditProfileForm,Form_permissions
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordResetDoneView
from django.utils import timezone
import pandas as pd
from django.shortcuts import render
from apps.personas.models import P04
from django.utils import timezone
import numpy as np
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import HttpResponseForbidden
from django.views.generic import CreateView,DeleteView,UpdateView
from apps.personas.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from apps.personas.forms import Form_rol
import json
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from decimal import Decimal
#MENSAJE DE CAMBIO DE CONTRASEÑA
class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('personas:perfil') 

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Contraseña cambiada exitosamente!')
        return response

#REFIRECCION DE EL HOME
def Home(request):
    
    return render(request, 'home.html')

#REGISTRO DE PERSONA

def Registro(request):
    if request.method == 'POST':
        formPersona = PersonaForm(request.POST)
        if formPersona.is_valid():
            user = formPersona.save(commit=False)
            user.set_password(formPersona.cleaned_data['password1'])
            user.save()

            # Asignar el rol 'Usuario' al nuevo usuario
            usuario_role, created = Rol.objects.get_or_create(rol_nombre='Usuario', defaults={'rol_descripcion': 'Rol de ususario'})
            
            content_type = ContentType.objects.get_for_model(user.__class__)
            user_permission, created = Permission.objects.get_or_create(
                codename='can_view_usuario_dashboard',
                content_type=content_type,
                defaults={'name': 'Can view usuario dashboard'}
            )
            usuario_role.permissions.add(user_permission)
            
            Persona_rol.objects.create(
                persona_id=user,
                rol_id=usuario_role,
                rolp_fecha_inicio=timezone.now(),
                rolp_fecha_fin=timezone.now(),  # O usa una fecha futura si es necesario
                rolp_estado=True
            )
            

            # Autenticación y login
            per_documento = formPersona.cleaned_data.get('per_documento')
            raw_password = formPersona.cleaned_data.get('password1')
            user = authenticate(username=per_documento, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, "¡Registro exitoso! Bienvenido.")
                return redirect('personas:inicio_sesion')
            else:
                messages.error(request, 'Error en autenticación')
        else:
            # Mostrar errores específicos del formulario
            for field in formPersona:
                for error in field.errors:
                    messages.error(request, f"Error en {field.label}: {error}")
            # También puedes mostrar errores generales
            for error in formPersona.non_field_errors():
                messages.error(request, error)
    else:
        formPersona = PersonaForm()
    return render(request, 'registro.html', {'formPersona': formPersona})



#INICIO DE SESION DE PERSONA
def inicio_sesion(request):
    if request.method == 'POST':
        formPersona = LoginForm(request.POST)
        if formPersona.is_valid():
            per_documento = formPersona.cleaned_data['per_documento']
            password = formPersona.cleaned_data['password1']
            user = authenticate(request, username=per_documento, password=password)
            if user is not None:
                login(request, user)
                return redirect('cores:general')  # Redirigir a la página principal u otra página
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        formPersona = LoginForm()
    return render(request, 'inicio_sesion.html', {'formPersona': formPersona})


#cerrar seion
def Cierre_sesion(request):
    logout(request)
    return redirect('personas:inicio_sesion')


#CONFIRMACION DE LA EXISTENCIAS DE UN CORREO ELECTRONICO
def validacion_email(request):
    email = request.GET.get('email')
    exists = Persona.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

def validar_documento(request):
    documento = request.GET.get('documento')
    exists = Persona.objects.filter(per_documento=documento).exists()
    return JsonResponse({'exists': exists})

#REDIRIGE AL PERFIL CON LOS DATOS EXISTENTES
def Perfil(request):
    formPersona = EditProfileForm
    return render(request, 'perfil.html',{'formPersona':formPersona})



#EDITAR PERFIL DE LA PERSONA
@login_required
def Editar_perfil(request, per_documento):
    persona = Persona.objects.get(per_documento=per_documento)
    
    if request.method == 'POST':
        formPersona = EditProfileForm(request.POST, request.FILES, instance=persona)
       
        if formPersona.is_valid():
            formPersona.save()
            return redirect(reverse('personas:editar_perfil', kwargs={'per_documento': per_documento}))
        
    else:
        formPersona = EditProfileForm(instance=persona)
        
    return render(request, 'perfil.html', {'formPersona': formPersona})


#captura el correo que se ingreso en el formulario
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        response = super().form_valid(form)
        return HttpResponseRedirect(f"{reverse_lazy('password_reset_done')}?email={email}")


#recibe el correo ingresado para visualizarlo
class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.GET.get('email')
        return context



@permission_required('can_view_reporteador_dashboard')
def p04(request):

    per_documento = Persona.objects.all()
    
    return render(request,'p04.html',  {'per_documento':per_documento})


def subir_P04(request):
    if request.method == 'POST':
        archivo = request.FILES.get('fileUpload')
        per_documento = request.POST.get('per_documento')
      
    
        if archivo and archivo.name.endswith(('.xlsx','.xls','xml')):
            try:
            
                if archivo.name.endswith('.xlsx'):
                    engine = 'openpyxl'
                elif archivo.name.endswith('.xls'):
                    engine = 'xlrd'
                
                else:
                    raise ValueError('Formato de archivo no soportado')
                
                
                selected_persona = Persona.objects.get(per_documento=per_documento)
                hoja_principal = 'Reporte'
                hoja_alternativa = 'Hoja1'
                
                
                hojas = pd.ExcelFile(archivo).sheet_names
                if hoja_principal in hojas:
                    df = pd.read_excel(archivo, header=4, sheet_name=hoja_principal)
                else:
                    df = pd.read_excel(archivo, header=0, sheet_name=hoja_alternativa)
                
           

                df['FECHA_INICIO_FICHA'] = pd.to_datetime(df['FECHA_INICIO_FICHA'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d') 
                df['FECHA_TERMINACION_FICHA'] = pd.to_datetime(df['FECHA_TERMINACION_FICHA'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d') 
               
                
 
 
                df = df.replace(r'^\s*$', np.nan, regex=True)
                
       
 

                
                
                # Itera sobre las filas del DataFrame
                for index, row in df.iterrows():
                    
                    nombre_programa = row['NOMBRE_PROGRAMA_FORMACION']
                    
                    if not Programa.objects.filter(nombre_programa_f=nombre_programa).exists():
                        
                        Programa.objects.create(nombre_programa_f=nombre_programa)
               
                    try:
                        
                        p, creado = P04.objects.update_or_create(
                        identificador_ficha =row['IDENTIFICADOR_FICHA'],
                        defaults={
                            'fecha_p04': timezone.now(),
                            'codigo_regional': row['CODIGO_REGIONAL'],
                            'nombre_regional': row['NOMBRE_REGIONAL'],
                            'codigo_centro': row['CODIGO_CENTRO'],
                            'nombre_centro': row['NOMBRE_CENTRO'],
                            'identificador_unico_ficha': row['IDENTIFICADOR_UNICO_FICHA'],
                            'estado_curso': row['ESTADO_CURSO'],
                            'codigo_nivel_formacion': row['CODIGO_NIVEL_FORMACION'],
                            'nivel_formacion': row['NIVEL_FORMACION'],
                            'codigo_jornada': row['CODIGO_JORNADA'],
                            'nombre_jornada': row['NOMBRE_JORNADA'],
                            'tipo_de_formacion': row['TIPO_DE_FORMACION'],
                            'fecha_inicio_ficha': row['FECHA_INICIO_FICHA'],
                            'fecha_terminacion_ficha': row['FECHA_TERMINACION_FICHA'],
                            'etapa_ficha': row['ETAPA_FICHA'],
                            'modalidad_formacion': row['MODALIDAD_FORMACION'],
                            'codigo_sector_programa': row['CODIGO_SECTOR_PROGRAMA'],
                            'nombre_sector_programa': row['NOMBRE_SECTOR_PROGRAMA'],
                            'codigo_ocupacion': row['CODIGO_OCUPACION'],
                            'nombre_ocupacion': row['NOMBRE_OCUPACION'],
                            'codigo_programa': row['CODIGO_PROGRAMA'],
                            'version_programa': row['VERSION_PROGRAMA'],
                            'nombre_programa_formacion': row['NOMBRE_PROGRAMA_FORMACION'],
                            'red': row['RED'] if 'RED' in df.columns else None,
                            'codigo_pais_curso': row['CODIGO_PAIS_CURSO'],
                            'nombre_pais_curso': row['NOMBRE_PAIS_CURSO'],
                            'codigo_departamento_curso': row['CODIGO_DEPARTAMENTO_CURSO'],
                            'nombre_departamento_curso': row['NOMBRE_DEPARTAMENTO_CURSO'],
                            'codigo_municipio_curso': row['CODIGO_MUNICIPIO_CURSO'],
                            'nombre_municipio_curso': row['NOMBRE_MUNICIPIO_CURSO'],
                            'codigo_convenio': row['CODIGO_CONVENIO'],
                            'nombre_convenio': row['NOMBRE_CONVENIO'],
                            'ampliacion_cobertura': row['AMPLIACION_COBERTURA'],
                            'codigo_programa_especial': row['CODIGO_PROGRAMA_ESPECIAL'],
                            'nombre_programa_especial': nombre_programa,
                            'numero_cursos': row['NUMERO_CURSOS'],
                            'total_aprendices_masculinos': row['TOTAL_APRENDICES_MASCULINOS'],
                            'total_aprendices_femeninos': row['TOTAL_APRENDICES_FEMENINOS'],
                            'total_aprendices_nobinario': row['TOTAL_APRENDICES_NOBINARIO'] if 'TOTAL_APRENDICES_NOBINARIO' in df.columns else None,
                            'total_aprendices': row['IDENTIFICADOR_FICHA'],
                            'duracion_programa': row['DURACION_PROGRAMA'],
                            'nombre_nuevo_sector': row['NOMBRE_NUEVO_SECTOR'],
                            'total_aprendices_activos': row['TOTAL_APRENDICES_ACTIVOS'],
                            'per_documento': selected_persona
                        }
                       )

                    except Exception as e:
                        print(f"Error al guardar el registro en la fila {index}: {e}")
                    

            
                messages.success(request, "Datos guardados exitosamente.")

            
            except Exception as e:
              messages.error(request, f"Error al procesar el archivo: {str(e)}")
        else:
            messages.error(request, "Por favor suba un archivo válido en formato .xlsx.")
        
        
    return redirect('personas:P04')
def contar_registros_p04():
    numero_registros_guardados_db = P04.objects.count()
    
@permission_required('can_view_reporteador_dashboard')
def Poblacion_vulnerable(request):
    
    per_documento = Persona.objects.all()

    return render( request, 'Poblacion_vulnerable/poblacion_vulnerable.html', {'per_documento':per_documento})
    
def Poblacion_vulnerable_graficas(request):
    
  
    
    datos_poblacion= Documento_vulnerables_poblaciones.objects.all()

    
    
     #envio de datos 
    cupos = 'Cupos'
    aprendices = 'Aprendices'
    poblacion_cupos = datos_poblacion.filter(grupos_poblaciones=cupos)
    poblacion_aprendices = datos_poblacion.filter(grupos_poblaciones=aprendices)
  
    def porcentajes(valor):
        conversiones_de_porcentajes = []
        for poblaciones_cupos in valor:
            datos_porcentaje= poblaciones_cupos.porcentaje_ejecucion_poblaciones 
            conversiones =datos_porcentaje * 100
            conversiones_de_porcentajes.append(conversiones)
    
        return conversiones_de_porcentajes
    
    conversiones_de_porcentajes_cupos = porcentajes(poblacion_cupos)
    conversiones_de_porcentajes_aprendices = porcentajes(poblacion_aprendices)
    
    
    
    #datos de grfica para los valores en ejecucion (array)
    def valores_grafica(valores):
        resultado = []
        for ejecucion in valores.values('ejecucion_poblaciones'):
           data_ejecucion = ejecucion['ejecucion_poblaciones']
           if isinstance(data_ejecucion, Decimal):
               data_ejecucion = float(data_ejecucion)
           
           resultado.append(data_ejecucion)
        
        return resultado
    #datos de grfica para las metas (array)
    def valores_grafica_meta(valores):
        resultado_meta = []
        for meta in valores.values('meta_2024_poblaciones'):
           data_meta = meta['meta_2024_poblaciones']
           if isinstance(data_meta, Decimal):
               data_meta = float(data_meta)
           
           resultado_meta.append(data_meta)
        
        return resultado_meta
    data_cupos_grafica = valores_grafica(poblacion_cupos)
    data_aprendices_grafica = valores_grafica(poblacion_aprendices)
    meta_cupos_grafica = valores_grafica_meta(poblacion_cupos)
    meta_aprendices_grafica = valores_grafica_meta(poblacion_aprendices)
   
    datos_grafica = data_cupos_grafica + data_aprendices_grafica
    meta_grafica = meta_cupos_grafica + meta_aprendices_grafica
    
    
    #DATOS PARA TIPO DE POBLACION
    
    
    datos_tipo_poblacion= Documento_vulnerables_tipo_poblaciones.objects.all()

    
    
     #envio de datos 
    cupos = 'Cupos'
    aprendices = 'Aprendices'
    tipo_poblacion_cupos = datos_tipo_poblacion.filter(grupo=cupos)
    tipo_poblacion_aprendices = datos_tipo_poblacion.filter(grupo=aprendices)
  
  
  
    #PORCENTAJE PARA TIPO DE POBLACION
    def porcentajes_tipo_poblacion(valor):
        conversiones_de_porcentajes = []
        for tipo_poblaciones in valor:
            datos_porcentaje= tipo_poblaciones.porcentaje_ejecucion
            conversiones =datos_porcentaje * 100
            conversiones_de_porcentajes.append(conversiones)
    
        return conversiones_de_porcentajes
    
    conversiones_de_porcentajes_cupos_tipo_poblacion = porcentajes_tipo_poblacion(tipo_poblacion_cupos)
    conversiones_de_porcentajes_aprendices_tipo_poblacion = porcentajes_tipo_poblacion(tipo_poblacion_aprendices)
    
    #datos de grfica para los valores en ejecucion (array)
    def valores_grafica_tipo_poblaciones(valores):
        resultado = []
        for ejecucion in valores.values('ejecucion'):
           data_ejecucion = ejecucion['ejecucion']
           if isinstance(data_ejecucion, Decimal):
               data_ejecucion = float(data_ejecucion)
           
           resultado.append(data_ejecucion)
        
        return resultado
    
    #datos de grfica para las metas (array)
    def valores_grafica_meta_tipo_poblaciones(valores):
        resultado_meta = []
        for meta in valores.values('meta_2024'):
           data_meta = meta['meta_2024']
           if isinstance(data_meta, Decimal):
               data_meta = float(data_meta)
           
           resultado_meta.append(data_meta)
        
        return resultado_meta
    
    data_cupos_grafica_tipo_poblaciones = valores_grafica_tipo_poblaciones(tipo_poblacion_cupos)
    data_aprendices_grafica_tipo_poblaciones = valores_grafica_tipo_poblaciones(tipo_poblacion_aprendices)
    meta_cupos_grafica_tipo_poblaciones = valores_grafica_meta_tipo_poblaciones(tipo_poblacion_cupos)
    meta_aprendices_grafica_tipo_poblaciones= valores_grafica_meta_tipo_poblaciones(tipo_poblacion_aprendices)
    
    data_tipo_poblaciones = data_cupos_grafica_tipo_poblaciones + data_aprendices_grafica_tipo_poblaciones
    meta_tipo_poblaciones = meta_cupos_grafica_tipo_poblaciones + meta_aprendices_grafica_tipo_poblaciones

    context = {
        'poblacion_cupos':poblacion_cupos,
        'poblacion_aprendices':poblacion_aprendices,
        'conversiones_de_porcentajes_cupos':conversiones_de_porcentajes_cupos,
        'conversiones_de_porcentajes_aprendices':conversiones_de_porcentajes_aprendices,
        'datos_grafica':json.dumps(datos_grafica),
        'meta_grafica':json.dumps(meta_grafica),
        'tipo_poblacion_cupos':tipo_poblacion_cupos,
       'tipo_poblacion_aprendices':tipo_poblacion_aprendices,
       'conversiones_de_porcentajes_cupos_tipo_poblacion':conversiones_de_porcentajes_cupos_tipo_poblacion,
       'conversiones_de_porcentajes_aprendices_tipo_poblacion':conversiones_de_porcentajes_aprendices_tipo_poblacion,
       'data_tipo_poblaciones':json.dumps(data_tipo_poblaciones),
       'meta_tipo_poblaciones':json.dumps(meta_tipo_poblaciones)
    }
    
    return render(request,'Poblacion_vulnerable/poblacion_vulnerable_graficas.html',context)



def Subir_poblacion_vulnerable(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        per_documento = request.POST.get('per_documento')
        selected_persona = Persona.objects.get(per_documento=per_documento)

        try:
            df = pd.read_excel(excel_file, sheet_name='RESUMEN', header=None)
            
            # TABLA TIPO DE POBLACIONES Y POBLACIONES
            # renombrar cabeceras
            df.iloc[18, 1] = 'Grupos'
            df.iloc[21, 1] = 'Porcentaje_ejecicion'
            df.iloc[7, 1] = 'Indicadores_poblaciones'
            df.iloc[8, 1] = 'Grupos_poblaciones'
            df.iloc[9, 1] = 'Meta_2024_poblaciones'
            df.iloc[10, 1] = 'Ejecucion_poblaciones'
            df.iloc[11, 1] = 'porcentaje_de_poblaciones'
            
            # rellenar grupos de nan a el valor anterior para poblaciones
            fila_remplazar_poblaciones = 7
            df.loc[fila_remplazar_poblaciones] = df.loc[fila_remplazar_poblaciones].fillna(method='ffill')

            # rellenar grupos de nan a el valor anterior para tipo de poblaciones
            fila_remplazar = 17
            df.loc[fila_remplazar] = df.loc[fila_remplazar].fillna(method='ffill')

            # rellenar fila con valor anterior para profesion integral
            fila_remplazar_profesion_nivel = 26
            fila_remplazar_profesion_sobreejecucion = 30

            df.loc[fila_remplazar_profesion_nivel] = df.loc[fila_remplazar_profesion_nivel].fillna(method='ffill')
            df.loc[fila_remplazar_profesion_sobreejecucion] = df.loc[fila_remplazar_profesion_sobreejecucion].fillna(method='ffill')

            # datos para formación profesional integral
            datos_profesion_integral = df.iloc[26:31, 2]
            encabezado_profesion_integral = [header.strip() for header in datos_profesion_integral]
            datos_profesion_integral = df.iloc[26:31, 3:5].values
            reorganizado_profesion_integral = pd.DataFrame(datos_profesion_integral.T, columns=encabezado_profesion_integral)

            # datos para población
            datos_poblaciones_encabezado = df.iloc[7:12, 1]
            encabezado_poblaciones = [header.strip() for header in datos_poblaciones_encabezado]
            datos_poblaciones = df.iloc[7:12, 2:12].values
            reorganizado_poblaciones = pd.DataFrame(datos_poblaciones.T, columns=encabezado_poblaciones)

            # datos tipo poblaciones
            datos = df.iloc[17:22, 1]
            encabezado = [header.strip() for header in datos]
            datos_documento = df.iloc[17:22, 2:].values
            reorganizado = pd.DataFrame(datos_documento.T, columns=encabezado)

            for _, row in reorganizado.iterrows():
                datos_vulnerables = Documento_vulnerables_tipo_poblaciones(
                    indicadores=row['Indicador'],
                    grupo=row['Grupos'],
                    meta_2024=row['Meta 2024'],
                    ejecucion=row['Ejecución'],
                    porcentaje_ejecucion=row['Porcentaje_ejecicion'],
                    per_documento=selected_persona
                )
                datos_vulnerables.save()

            for _, row in reorganizado_poblaciones.iterrows():
                datos_poblaciones = Documento_vulnerables_poblaciones(
                    indicadores_poblaciones=row['Indicadores_poblaciones'],
                    grupos_poblaciones=row['Grupos_poblaciones'],
                    meta_2024_poblaciones=row['Meta_2024_poblaciones'],
                    ejecucion_poblaciones=row['Ejecucion_poblaciones'],
                    porcentaje_ejecucion_poblaciones=row['porcentaje_de_poblaciones'],
                    per_documento=selected_persona
                )
                datos_poblaciones.save()

            for _, row in reorganizado_profesion_integral.iterrows():
                datos_profesion_integral_save = Formacion_profesional_integral(
                    nivel_ejecucion=row['Nivel de Ejecución'],
                    buena=row['Buena'],
                    vulnerable=row['Vulnerable'],
                    baja=row['Baja'],
                    sobreejecucion=row['Sobreejecución'],
                )
                datos_profesion_integral_save.save()

            # Mensaje de éxito general
            messages.success(request, 'Todos los datos se han guardado exitosamente.')

        
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')

        else:
            messages.error(request, 'El archivo no es un archivo Excel válido.')

        return redirect('personas:poblacion_vulnerable')

#CRUD DE ROL
def Roles_index(request):
    
    roles  = Rol.objects.all()
    form_roles = Form_rol
    
    context = {
        'roles':roles,
        'form_roles':form_roles
    }
    return render(request,'Roles/roles.html',context)

class Roles_create(CreateView):
    model = Rol
    form_class = Form_rol
    template_name = 'Roles/roles.html'
    success_url= reverse_lazy('personas:roles_index')
    
    
    def get(self, request, *args, **kwargs):
        permiso = request.GET.get('permissions')
        
        
    
    def form_valid(self, form):
        print('entro al formulario')
        if form.is_valid():
            
             response = super().form_valid(form)
        else:
            
             print('jshdgfjhdsgf', form.errors)
        permissions = form.cleaned_data.get('permissions').id
        print('permiso', permissions)
        
        if permissions:
            self.object.permissions.add(permissions)
            
          
        return response

    def form_invalid(self, form):
        print('errororororororor', form.errors)
        return super().form_invalid(form)
class Roles_delete(DeleteView):
    model = Rol
    success_url = reverse_lazy('personas:roles_index')
    
class Roles_edit(UpdateView):
    model = Rol
    form_class = Form_rol
    success_url = reverse_lazy('personas:roles_index')
    
    
#CRUD DE PERMISOS

def Permisos_index(request):
    permisos = Permission.objects.all().order_by('-id')
    forms_permisos = Form_permissions
    
    context = {
        'permisos':permisos,
        'forms_permisos':forms_permisos
    }
    
    return render(request, 'Permisos/permisos.html', context)
    
class Permisos_create(CreateView):
    model = Permission
    form_class = Form_permissions
    template_name = 'Permisos/permisos.html'
    success_url = reverse_lazy('personas:permisos_index')
    
    
    def form_valid(self, form):
        permission = form.save(commit=False)
        
        permission.content_type = ContentType.objects.get_for_model(Persona)
        permission.save()
        
        return super().form_valid(form)

class Permisos_delete(DeleteView):
    model = Permission
    success_url = reverse_lazy('personas:permisos_index')
    
class Permisos_edit(UpdateView):
    model = Permission
    form_class = Form_permissions
    success_url = reverse_lazy('personas:permisos_index')
    