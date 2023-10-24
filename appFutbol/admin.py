from django.contrib import admin
from .models import Usuario, Recinto, Reserva, Partido, Jugadores_partido, Equipo, Torneo, Resultado, DatosUsuario, Posts

# Register your models here.

misModelos = [
    Usuario, 
    Recinto, 
    Reserva, 
    Partido, 
    Jugadores_partido,
    Equipo,
    Torneo,
    Resultado,
    DatosUsuario,
    Posts
    ]
admin.site.register(misModelos)