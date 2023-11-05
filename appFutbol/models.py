from django.conf import settings
from django.db import models
# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    nivel = models.FloatField(default=0.0, db_column="puntos_usuario")
    telefono = models.CharField(max_length=9)


class Recinto(models.Model):
    nombre = models.TextField()
    ubicacion = models.TextField()
    telefono = models.CharField(max_length=9)
    
    def __str__(self) -> str:
        return self.nombre


class Reserva(models.Model):
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
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="creador_reserva")
    campo_reservado = models.OneToOneField(Recinto, on_delete=models.CASCADE)


class Partido(models.Model):
    ESTILO = [
        (5, "Fútbol sala"),
        (7, "Fútbol 7"),
        (11, "Fútbol 11"),
    ]
    estilo = models.CharField(max_length=1, choices=ESTILO)
    #--------Relaciones--------
    usuarios_jugadores = models.ManyToManyField(Usuario, through="Jugador_partido", related_name="jugadores_partido")
    reserva_partido = models.OneToOneField(Reserva, on_delete=models.CASCADE)


class Jugador_partido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    GANADOR = [
        ("S", "Sí"),
        ("N","No")
    ]
    ganar = models.CharField(max_length=1, choices=GANADOR)


class Equipo(models.Model):
    LOCALIA = [
        ("LO", "Local"),
        ("VI", "Visitante")
    ]
    localia = models.CharField(max_length=2, choices=LOCALIA)


class Torneo(models.Model):
    equipos = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    partidos = models.ManyToManyField(Partido)


class Resultado(models.Model):
    goles_local = models.IntegerField(verbose_name="Goles local")
    goles_visitante = models.IntegerField(verbose_name="Goles visitante")
    #--------Relaciones--------
    resultado_partido = models.OneToOneField(Partido, on_delete=models.CASCADE)


class DatosUsuario(models.Model):
    descripcion = models.TextField()
    POSICION = [
        ("GOA","Portero"),
        ("DEF","Defensa"),
        ("MID","Centrocampista"),
        ("STR", "Delantero")
    ]
    posicion = models.CharField(max_length=3, choices=POSICION)
    ubicacion = models.TextField()
    #--------Relaciones--------
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="datos_usuario")
    partidos_jugados = models.ManyToManyField(Partido)


class Post(models.Model):
    contenido = models.TextField()
    #--------Relaciones--------
    creador_post = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="creador_post")