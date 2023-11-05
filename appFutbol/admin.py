from django.contrib import admin
from .models import Usuario, Recinto, Reserva, Partido, Jugador_partido, Equipo, Torneo, Resultado, DatosUsuario, Post

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
    Post
    ]
admin.site.register(misModelos)