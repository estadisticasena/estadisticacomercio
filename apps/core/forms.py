from apps.personas.models import Meta
from apps.core.models import  Bilinguismo_programa,Regional, Nivel_formacion
from apps.personas.models import Metas_formacion,Modalidad,Estrategia, Estrategia_detalle,Persona,Centro_de_formacion
from django.core.exceptions import ValidationError
from django import forms
class Form_meta(forms.ModelForm):
    
    
    class Meta:
        model = Meta
        fields = [
        
        
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
        'per_documento'
        ]
        
        widgets =  {
            'met_fecha_inicio': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'met_fecha_fin': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            
            'met_codigo': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion'}),
            'met_año': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_otras_poblaciones': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_victimas': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_hechos_victimizantes': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_desplazados_violencia': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_titulada': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_complementaria': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_total_poblacion_vulnerable': forms.TextInput(attrs={'class':'form-control','aria-label':'Centro de formacion','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            
           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['per_documento'].widget =  forms.HiddenInput()
       
    def clean_meta_año(self):
        met_años = self.cleaned_data.get('met_año')
        if Meta.objects.filter(met_año=met_años).exists():
            raise forms.ValidationError('Este año ya existe')
        
       
        if len(str(met_años)) > 4:
            raise ValidationError('El año no puede tener mas de 4 caracteres')
        return met_años
    
class Form_meta_formacion(forms.ModelForm):
    
    
    class Meta:
        model = Metas_formacion
        fields = [
            'metd_id',
            'met_centro_formacion',
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
            'met_id',
            
            
        ]
        widgets =  {
            'metd_modalidad': forms.Select(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_centro_formacion': forms.Select(attrs={'class':'form-control'}),
            'met_formacion_operario': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_auxiliar': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_tecnico': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_profundizacion_tecnica': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_tecnologo': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_evento': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_curso_especial': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_bilinguismo': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_formacion_sin_bilinguismo': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'met_id': forms.Select(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),

            
        }
    
    

#ESTRATEGIAS INSTITUCINALES


class Form_estrategias(forms.ModelForm):
    
    
    class Meta:
        model = Estrategia
        fields = [
         
            'est_nombre',

        ]
        widgets =  {
            'est_nombre': forms.TextInput(attrs={'class':'form-control'}),

         }


        
        
class Form_meta_estrategia_detalle(forms.ModelForm):

 
    class Meta: 
        model = Estrategia_detalle
        fields = {
            "est_id",
            'estd_modalidad',
            'estd_operario_meta',
            'estd_auxiliar_meta',
            'estd_tecnico_meta',
            'estd_profundizacion_tecnica_meta',
            'estd_tecnologo',
            'estd_evento',
            'estd_curso_especial',
            'estd_bilinguismo',
            'estd_sin_bilinguismo',
            'estd_meta',
        }
        widgets =  {
            'estd_meta': forms.Select(attrs={'class':'form-control'}),
            'estd_modalidad': forms.Select(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'est_id': forms.Select(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'estd_operario_meta': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'estd_auxiliar_meta': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'estd_tecnico_meta': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'estd_profundizacion_tecnica_meta': forms.TextInput(attrs={'class':'form-control'}),
            'estd_tecnologo': forms.TextInput(attrs={'class':'form-control'}),
            'estd_evento': forms.TextInput(attrs={'class':'form-control',}),
            'estd_curso_especial': forms.TextInput(attrs={'class':'form-control'}),
            'estd_bilinguismo': forms.TextInput(attrs={'class':'form-control'}),
            'estd_sin_bilinguismo': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
  
           

        }
        
 
        
class Form_modalidad(forms.ModelForm):
    
    class Meta:
        model = Modalidad
        fields = [
            'modalidad'
        ]
    
        
    
    
class Form_Bilinguismo_programa(forms.ModelForm):
    class Meta:
        model = Bilinguismo_programa
        fields = [
            'bil_codigo',
            'bil_version',
            'bil_modalidad',
            'Bil_programa',
            'bil_duracion'

        ]
        widgets =  {
            'bil_codigo': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'bil_version': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
            'bil_modalidad': forms.Select(attrs={'class':'form-control'}),
            'Bil_programa': forms.TextInput(attrs={'class':'form-control'}),
            'bil_duracion': forms.TextInput(attrs={'class':'form-control','oninput': 'this.value = this.value.replace(/[^0-9]/g, "");'}),
        }

class Form_centro_de_formacion(forms.ModelForm):
    
    class Meta:
        model = Centro_de_formacion
        fields = [
            'centro_de_formacion'
        ]
        widgets =  {
            'centro_de_formacion': forms.TextInput(attrs={'class':'form-control'}),
        }
        
class Form_regional(forms.ModelForm):
    
    class Meta:
        model = Regional
        fields = [
            'regional'
        ]
        widgets =  {
            'regional': forms.TextInput(attrs={'class':'form-control'}),
        }

class Form_nivel_formacion(forms.ModelForm):
    
    class Meta:
        model = Nivel_formacion
        fields = [
            'nivel_formacion'
        ]
        widgets =  {
            'nivel_formacion': forms.TextInput(attrs={'class':'form-control'}),
        }