from django import forms
from .models import Persona
from .models import P04
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from apps.personas.models import Rol
from django.contrib.auth.models import Permission

#FORMS DE REGISTRO
class PersonaForm(UserCreationForm):
    
    email = forms.EmailField(required=True, label="Correo electrónico", max_length=50, help_text="Coloca tu correo electrónico", error_messages={'invalid': 'Solo puedes colocar caracteres válidos para el email'})
 
    
    class Meta:
        model = Persona
        fields = ['per_documento', 'per_tipo_documento', 'email', 'per_nombres', 'per_apellidos', 'per_telefono', 'password1', 'password2']
        Widget = {
            'per_tipo_documento': forms.Select(attrs={'class':'form-control'})
        }
        
    #validaciones
    def clean_per_correo(self):
        email = self.cleaned_data.get('email').lower()
        if Persona.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya ha sido tomado")
        return email
    

    
    def save(self, commit=True):
        user = super(PersonaForm, self).save(commit=False)
        user.per_correo = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

#FORMS DE INICIO DE SESION
class LoginForm(forms.Form):
    per_documento = forms.IntegerField(label='Documento de identidad')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    
    def clean_per_documento(self):
        per_documento = self.cleaned_data['per_documento']
        # No es necesario validar con isdigit() para un IntegerField
        return per_documento

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8 or not any(char.isdigit() for char in password1) or not any(char.isalpha() for char in password1):
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres y contener números y letras.")
        return password1


#FORMS DE EDITAR PERFIL
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('per_documento', 'per_tipo_documento', 'per_nombres', 'per_apellidos', 'email', 'per_telefono','per_image')
        Widget = {
            'per_tipo_documento': forms.Select(attrs={'class':'form-control'})
        }
        



class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()


class Form_rol(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all().order_by('-id'), required=True, widget=forms.Select)
    class Meta:
        model = Rol
        fields = [
            'rol_nombre', 'rol_descripcion','permissions'
        ]
      
class Form_permissions(forms.ModelForm):
    class Meta:
        model = Permission
        fields = [
            'name','codename'
        ]
        # estableces el campo directamente a la hora de crearlo ene lepost 