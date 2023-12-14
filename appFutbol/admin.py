from django.contrib import admin
from .models import Usuario, Recinto, Partido, Jugador_partido, Resultado, DatosUsuario, Post, Votacion_partido, Cuenta_bancaria, Promocion

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
    Cuenta_bancaria
    ]
admin.site.register(misModelos)