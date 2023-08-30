from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('login', auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True),name='login'),
    path('login_user', views.login_user, name="login-user"),
    path('registrarUsuario', views.registrarUsuario, name="registrar-usuario"),
    path('logout', views.logoutuser, name='logout'),

    path('perfil', views.perfil, name='perfil'),
    path('actualizarPerfil', views.actualizarPerfil, name='actualizar_perfil'),
    path('actualizarContrasena', views.actualizarContrasena, name='actualizar_contrasena'),

    path('', views.inicio, name='inicio'),

    path('empresa', views.empresa, name='empresa-pagina'),
    path('adm_empresa', views.adm_empresa, name='adm-empresa'),
    path('guardar_empresa', views.guardar_empresa, name='guardar-empresa'),
    path('adm_empresa/<int:pk>', views.adm_empresa, name='adm-empresa-pk'),
    path('eliminar_empresa', views.eliminar_empresa, name='eliminar-empresa'),

    path('sede', views.sede, name='sede-pagina'),
    path('adm_sede', views.adm_sede, name='adm-sede'),
    path('guardar_sede', views.guardar_sede, name='guardar-sede'),
    path('adm_sede/<int:pk>', views.adm_sede, name='adm-sede-pk'),
    path('eliminar_sede', views.eliminar_sede, name='eliminar-sede'),

    path('bus', views.bus, name='bus-pagina'),
    path('adm_bus', views.adm_bus, name='adm-bus'),
    path('guardar_bus', views.guardar_bus, name='guardar-bus'),
    path('adm_bus/<int:pk>', views.adm_bus, name='adm-bus-pk'),
    path('eliminar_bus', views.eliminar_bus, name='eliminar-bus'),

    path('programado', views.programado, name='programacion-pagina'),
    path('adm_programado', views.adm_programado, name='adm-programado'),
    path('guardar_programado',views.guardar_programado,name='guardar-programado'),
    path('adm_programado/<int:pk>',views.adm_programado,name='adm-programado-pk'),
    path('eliminar_programado', views.eliminar_programado, name='eliminar-programado'),


    #schedule_trips schedule_trips.html
    path('viajes_programados',views.viajes_programados,name='viajes-programados-pagina'),

    path('adm_despachado/',views.adm_despachado,name='manage-despachado'),
    path('adm_despachado/<int:schedPK>',views.adm_despachado),
    path('save_despachado', views.save_despachado, name='save-book'),
    #booking despacho #schedule programado

    path('despachado',views.despachados,name='despachos-pagina'),
    path('view_despachado/<int:pk>',views.view_despachado,name='view-despachado'),
    path('pay_despachado',views.pay_despachado,name='pay-despachado'),
    path('delete_despachado',views.delete_despachado,name='delete-despachado'),

    path('buscar_programado',views.buscar_programado,name='buscar-viaje-programado'),


]


    #findtrips0car_programado,name='buscar-viaje-programado'),

