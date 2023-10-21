from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):
    nombre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    nivel = models.FloatField(default=0.0, db_column="puntos_usuario")
    telefono = models.CharField(max_length=9)


class Recinto(models.Model):
    nombre = models.TextField()
    ubicacion = models.TextField()
    telefono = models.CharField(max_length=9)
    #--------Relaciones--------


class Reserva(models.Model):
    id = models.IntegerField(unique=True)
    ESTADO = [
        ("F", "Completo"),
        ("A", "Disponible")
    ]
    estado = models.CharField(max_length=1, choices=ESTADO)
    TIPO = [
        ("Pr", "Privada"),
        ("Pu", "Pública")
    ]
    tipo = models.CharField(max_length=2, choices=TIPO)
    n_jugadores = models.IntegerField()
    #--------Relaciones--------
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    campo = models.ForeignKey(Recinto, on_delete=models.CASCADE)


class Partido(models.Model):
    id = models.IntegerField(unique=True)
    ESTILO = [
        (5, "Fútbol sala"),
        (7, "Fútbol 7"),
        (11, "Fútbol 11"),
    ]
    estilo = models.CharField(max_length=1, choices=ESTILO)
    #--------Relaciones--------
    usuarios_jugadores = models.ManyToManyField(Usuario, through="Jugadores_partido")
    juego = models.OneToOneField(Reserva, on_delete=models.CASCADE)


class Jugadores_partido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    GANADOR = [
        ("S", "Sí"),
        ("N","No")
    ]
    ganar = models.CharField(max_length=1, choices=GANADOR)


class Torneo(models.Model):
    pass 


class Equipo(models.Model):
    LOCALIA = [
        ("LO", "Local"),
        ("VI", "Visitante")
    ]
    localia = models.CharField(max_length=2, choices=LOCALIA)


class Resultado(models.Model):
    goles_local = models.IntegerField(verbose_name="Goles local", null=False)
    goles_visitante = models.IntegerField(verbose_name="Goles visitante", null=False)
    #--------Relaciones--------
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE)


class DatosUsuario(models.Model):
    descripcion = models.TextField()
    POSICION = [
        ("GOA","Portero"),
        ("DEF","Defensa"),
        ("MID","Centrocampista"),
        ("STR", "Delantero")
    ]
    posicion = models.CharField(max_length=2, choices=POSICION)
    partidos = models.ManyToManyField(Partido)
    ubicacion = models.TextField()
    #--------Relaciones--------
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Posts(models.Model):
    pass