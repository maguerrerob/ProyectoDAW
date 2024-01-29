from django.urls import path
from  .api_views import *

urlpatterns = [
    # Consulta sencilla a modelo principal
    path('partidos', partido_list),
    # Consulta mejorada
    path("partidos_mejorada", partido_list_mejorada),
    path("recintos/busqueda_simple", recinto_busqueda_simple),
    path("recintos/busqueda_avanzada", recinto_buscar_avanzado),
    # URL JWT mejorada
    path("datosusuarios", datosusuarios_list)
]