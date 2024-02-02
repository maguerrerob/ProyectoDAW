from django.contrib import admin
from .models import *

# Register your models here.

misModelos = [
    Usuario, 
    Recinto,
    Partido, 
    Jugador_partido,
    Resultado,
    DatosUsuario,
    Post,
    Votacion_partido,
    Cuenta_bancaria,
    Cliente,
    Dueñorecinto
    ]
admin.site.register(misModelos)