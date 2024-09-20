from django.contrib import admin
from apps.personas.models import Persona,Rol,Persona_rol
from django.contrib.auth.models import Permission
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('rol_id','rol_nombre','rol_descripcion')


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('per_documento','per_tipo_documento','email','per_nombres','per_apellidos','per_telefono','is_staff','is_active','is_superuser')


@admin.register(Persona_rol)
class Persona_rol_admin(admin.ModelAdmin):
    list_display = ('rolp_id','rolp_fecha_inicio','rolp_fecha_fin','rolp_estado')
    
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type','codename')
