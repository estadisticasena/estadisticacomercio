from django.contrib.auth.models import BaseUserManager,Permission,ContentType

from django.utils import timezone
class UsuarioManage(BaseUserManager):
    
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('El correo es obligatotio')
        
        email = self.normalize_email(email)
        personas = self.model(email=email, **kwargs)
        
        if password:
            personas.set_password(password)
            
        else:
            raise('La contraseña es obligatoria')
        
        personas.save(using=self._db)
        
        return personas
    
    def create_superuser(self, email, password=None, **kwargs):
        from apps.personas.models import Rol, Persona_rol
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        
        if kwargs.get('is_staff') is not True:
            raise ValueError('Is_staff must have is_staff=true')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Is_staff must have is_superuser=true')
        
        superuser = self.create_user(email, password, **kwargs)
        
    
        admin_role, created = Rol.objects.get_or_create(rol_nombre='Admin', defaults={'rol_descripcion': 'Administrador del sistema'})
        
        content_type = ContentType.objects.get_for_model(superuser.__class__)
        admin_permission, created = Permission.objects.get_or_create(
            codename='can_view_admin_dashboard',
            content_type=content_type,
            defaults={'name': 'Can view admin dashboard'}
        )
        admin_role.permissions.add(admin_permission)
        
        Persona_rol.objects.create(persona_id=superuser, rol_id=admin_role, rolp_fecha_inicio=timezone.now(),rolp_fecha_fin=timezone.now())

        return superuser