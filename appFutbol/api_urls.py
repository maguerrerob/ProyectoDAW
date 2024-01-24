from django.urls import path
from  .api_views import *

urlpatterns = [
    path('partidos', partido_list),
    path("recintos/busqueda_simple", recinto_busqueda_simple),
    
]