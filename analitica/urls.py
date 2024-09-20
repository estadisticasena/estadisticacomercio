"""
URL configuration for analitica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.core import views
from django.contrib.auth import views as auth_views
from apps.personas import views as persona_views

from apps.personas.views import CustomPasswordResetView, CustomPasswordResetDoneView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.personas.urls')),
    path('',include('apps.core.urls')),

    #COBERTURA
    



    
  

    

    path('grafica', views.grafica, name="grafica"),
  
    
    path('administrador/', views.administrador, name="administrador"),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('validacion_email/', persona_views.validacion_email, name='validacion_email'),
    path('validar_documento/', persona_views.validar_documento, name='validar_documento'),
    

]
