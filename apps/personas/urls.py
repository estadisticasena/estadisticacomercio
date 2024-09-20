from django.urls import path
from apps.personas.views import CustomPasswordChangeView
from apps.personas import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
app_name = 'personas'

urlpatterns = [
    path('registro/',views.Registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cierre_sesion/', views.Cierre_sesion, name='cierre_sesion'),
    path('home/', views.Home, name='Home'),
    path('perfil/', views.Perfil, name="perfil"),
    path('editar_perfil/<int:per_documento>/', views.Editar_perfil, name="editar_perfil"),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    
    #archivos
    path('subir_P04/', views.subir_P04, name='subir_P04'),
    path('P04/', views.p04, name="P04"),
    path('upload/', views.Subir_poblacion_vulnerable, name='upload_excel'),
    path('poblacion_vulnerable/index/', views.Poblacion_vulnerable, name="poblacion_vulnerable"),
    path('poblacion_vulnerable_graficas/', views.Poblacion_vulnerable_graficas, name="poblacion_vulnerable_graficas"),
    #CRUD DE ROL
    path('roles/index/',views.Roles_index, name="roles_index"),
    path('roles/create/',views.Roles_create.as_view(), name="roles_create"),
    path('roles/delete/<int:pk>',views.Roles_delete.as_view(), name="roles_delete"),
    path('roles/edit/<int:pk>',views.Roles_edit.as_view(), name="roles_edit"),
    #CRUD DE PERMISO
    path('permisos/index/',views.Permisos_index, name="permisos_index"),
    path('permisos/create/',views.Permisos_create.as_view(), name="permisos_create"),
    path('permisos/delete/<int:pk>',views.Permisos_delete.as_view(), name="permisos_delete"),
    path('permisos/edit/<int:pk>',views.Permisos_edit.as_view(), name="permisos_edit"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
