
CREDENCIALES SUPERUSUSERIO
#superusuario = nombre admin, correo estadisticasenacomercio@gmail.com, documento=123456789 contraseña=sena12345


CORREO PARA EL PROYECTO 
estadisticasenacomercio@gmail.com
Contraseña=estadistica
INICIAR PROYECTO:
terminal:
1) Activar entorno virtual

mac= source .venv/scripts/activate
windo = .venv/scripts/activate

2) ejecutar proyecto
mac= python3 manage.py runserver 
wind = python manage.py runserver 

3) actualizar requirements
pip freeze > requirements.txt  
4) actualizar entorno
pip install -r requirements.txt

CREACION DE ROLES CON PERMISOS

1) ingreso al admin de django
2) en la tabla Permissions = creo un nuevo permiso 
3) ejemplo =  campo name =Can View Reporteador dashboard
              campo content type = (siempre Personas|persona)
              campo codename = can_view_reporteador_dashboard (ejm) 
4) save

ROL
1) en la tabla rol, creo un nuevo rol
2) rol nombre = reporteador
   rol descripcion  = reporteador del sistema
   Permissions (selecciono el nuevo permiso en este caso) = Personas|persona|Can view Reporteador dashboard

Habilitar el permiso para las diferentes funciones y templates
1) (para funciones o clases)

 
  @permission_required('can_view_admin_dashboard')
  def administrador(request):
  pass
   
2) (para vistas/templates) 
   {% if perms.can_view_admin_dashboard %}               
         <span>Roles</span>           
   {% endif %}

El proyecto tiene configurados dos repositorios 
verificar = git remote -v 
para el reposiitorio de tecnoparque es necesario hacer push de esta manera:
git push new-origin main