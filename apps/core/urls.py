from django.urls import path
from apps.core import views as core_views


app_name = 'cores'
urlpatterns = [
 
    path('cobertura/index', core_views.cobertura, name="cobertura"),
    path('cobertura_mapa/', core_views.Cobertura_mapa.as_view(), name='cobertura_mapa'),
    path('programa/index', core_views.Programa_index, name="programa_index"),
    path('programa/', core_views.Programa.as_view(), name='programa'),
    path('ficha/<int:identificador_ficha>/', core_views.detalle_ficha, name='detalle_ficha'),
    path('desercion', core_views.Desercion.as_view(), name="Desercion"),
    path('formacion_regular/index', core_views.Formacion_regular_index, name='formacion_regular_index'),
    path('metas/create/', core_views.Meta_create.as_view(), name="meta_create"),
    path('metas_formacion/create/', core_views.Meta_formacion_create.as_view(), name="meta_formacion_create"),
    path('estrategias_institucionales/index/', core_views.Estrategias_institucionales_index, name='estrategias_institucionales_index'),
    path('estrategias/create/', core_views.Estrategias_create.as_view(), name='estrategias_create'),
    path('estrategias/est_total_meta/<int:met_id>/', core_views.get_meta_valores, name='est_total_meta'),
    path('meta_estrategia_detalle/create', core_views.Meta_estrategia_detalle.as_view(), name="meta_estrategia_detalle"),
    path('get_estrategia_data/<int:id_estd_modalidad>/', core_views.get_estrategia_data, name='get_estrategia_data'),
    path('meta_data/<int:id_estd_meta>/', core_views.meta_data, name='meta_data'),
    path('meta_detalle/<int:estd_meta>/', core_views.meta_detalle, name='meta_detalle'),
    path('filtrar_datos_y_modalidades/',core_views.metas_formacion_filtros.as_view(), name='filtrar_datos_y_modalidades'),
    path('filtrar_estrategias_institucionales/',core_views.estrategias_institucionales_filtros.as_view(), name='filtrar_estrategias_institucionales'),
    path('get_meta/<int:meta_id>/', core_views.get_meta, name='get_meta'),
    #MODALIDAD
    path('modalidad/index/', core_views.Modalidad_index, name='modalidad_index'),
    path('modalidad/create/', core_views.Modalidad_create.as_view(), name='modalidad_create'),
    path('modalidad/delete/<int:pk>', core_views.Modalidad_delete.as_view(), name='modalidad_delete'),
    path('modalidad/edit/<int:pk>', core_views.Modalidad_edit.as_view(), name='modalidad_edit'),
    
    #ROLES
    path('asignacion_roles/', core_views.Asignacion_roles, name="asignacion_roles" ),
    
    #GRAFICAS GENERAL
    path('general/index', core_views.general, name="general"),
    
    #estrategias institucionales graficas 
    path('estrategias/index', core_views.estrategias, name="estrategias_index"),
    #ALERTAS
    path('verificar-año/', core_views.Verificar_año, name='verificar_año'),
    #verificaciones de formularios meta formacion 
    path('verificacion_meta_formacion_regular/', core_views.Verificacion_meta_formacion_regular, name="verificacion_meta_formacion_regular"),
    
    #eliminar y editar meta formacion (formacion regular)
    path('meta_formacion/delete/<int:pk>', core_views.Meta_formacion_delete.as_view(), name="verificacion_meta_formacion_regular"),
    path('meta_formacion/edit/<int:pk>', core_views.Meta_formacion_edit.as_view(), name="meta_formacion_regular_edit"),
    #eliminar y editar estrategias institucionales (estrategia)
    path('estrategia_institucional/delete/<int:pk>', core_views.estrategia_institucional_delete.as_view(), name='estrategia_institucional_delete'),
    path('estrategia_institucional/edit/<int:pk>', core_views.estrategia_institucional_edit.as_view(), name='estrategia_institucional_edit'),
    #eliminar y editar  meta estrategia (estrategias institucionales)

    path('meta_estrategias_intitucionales/delete/<int:pk>', core_views.meta_estrategias_intitucionales_delete.as_view(), name='meta_estrategias_intitucionales_delete'),
    path('meta_estrategias_intitucionales/edit/<int:pk>', core_views.meta_estrategias_intitucionales_edit.as_view(), name='meta_estrategias_intitucionales_edit'),
    
    #eliminar y editar  meta estrategia (estrategias institucionales)
    path('meta/edit/<int:pk>', core_views.meta_edit.as_view(), name='meta_edit'),
    path('meta/delete/<int:pk>', core_views.meta_delete.as_view(), name='meta_delete'),
    path('meta/index/', core_views.meta_index, name='meta_index'),
    
    #BILINGUISMO
    path('bilinguismo/index/', core_views.Bilinguismo_index, name='bilinguismo_index'),
    path('bilinguismo/create/', core_views.Bilinguismo_create.as_view(), name='bilinguismo_create'),
    path('bilinguismo/delete/<int:pk>', core_views.Bilinguismo_delete.as_view(), name='bilinguismo_delete'),
    path('bilinguismo/edit/<int:pk>', core_views.Bilinguismo_edit.as_view(), name='bilinguismo_edit'),
    #CENTRO_DE_FORMACION
    path('centro_de_formacion/index/', core_views.Centro_de_formacion_index, name='centro_de_formacion_index'),
    path('centro_de_formacion/create/', core_views.Centro_de_formacion_create.as_view(), name='centro_de_formacion_create'),
    path('centro_de_formacion/delete/<int:pk>', core_views.Centro_de_formacion_delete.as_view(), name='centro_de_formacion_delete'),
    path('centro_de_formacion/edit/<int:pk>', core_views.Centro_de_formacion_edit.as_view(), name='centro_de_formacion_edit'),
    #REGIONAL
    path('regional/index/', core_views.Regional_index, name='regional_index'),
    path('regional/create/', core_views.Regional_create.as_view(), name='regional_create'),
    path('regional/delete/<int:pk>', core_views.Regional_delete.as_view(), name='regional_delete'),
    path('regional/edit/<int:pk>', core_views.Regional_edit.as_view(), name='regional_edit'),
    
    #NIVEL FORMACION
    path('nivel_formacion/index/', core_views.Nivel_formacion_index, name='nivel_formacion_index'),
    path('nivel_formacion/create/', core_views.Nivel_formacion_create.as_view(), name='nivel_formacion_create'),
    path('nivel_formacion/delete/<int:pk>', core_views.Nivel_formacion_delete.as_view(), name='nivel_formacion_delete'),
    path('nivel_formacion/edit/<int:pk>', core_views.Nivel_formacion_edit.as_view(), name='nivel_formacion_edit'),
    


]   


