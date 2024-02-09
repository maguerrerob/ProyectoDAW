from django.urls import path
from  .api_views import *

urlpatterns = [
    # Consulta sencilla a modelo principal
    path('partidos', partido_list),
    # Consulta mejorada
    path("partidos_mejorada", partido_list_mejorada),
    path('partido/<int:partido_id>',partido_obtener),
    path("partido/editar/<int:partido_id>", partido_editar_api),
    # URLs token oauth2 mejorada
    path("datosusuarios", datosusuarios_list),
    path("recintos/listar", recintos_list),
    # URLs token JWT
    path("posts/listar", posts_listar),
    path("recintos/busqueda_simple", recinto_busqueda_simple),
    path("recintos/busqueda_avanzada", recinto_buscar_avanzado),
    path("datosusuario/busqueda_avanzada", datosusuario_busqueda_avanzada),
    path("partidos/busqueda_avanzada", partido_buscar_avanzado),
    path("partido/crear", partido_create),
    path("clientes/listar", clientes_list),
]