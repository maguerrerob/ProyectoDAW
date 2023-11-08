from django.contrib import admin
from .models import Usuario, Recinto, Reserva, Partido, Jugador_partido, Equipo, Torneo, Resultado, DatosUsuario, Post, Votacion_partido, Cuenta_bancaria

# Register your models here.

misModelos = [
    Usuario, 
    Recinto, 
    Reserva, 
    Partido, 
    Jugador_partido,
    Equipo,
    Torneo,
    Resultado,
    DatosUsuario,
    Post,
    Votacion_partido,
    Cuenta_bancaria
    ]
admin.site.register(misModelos)