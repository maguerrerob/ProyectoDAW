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

class Equipo(models.Model):
    LOCALIA = [
        ("LO", "Local"),
        ("VI", "Visitante")
    ]
    localia = models.CharField(max_length=2, choices=LOCALIA)
    ESTILO = [
        (5, "Fútbol sala"),
        (7, "Fútbol 7"),
        (11, "Fútbol 11"),
    ]
    estilo = models.CharField(max_length=2, choices=ESTILO)

class Partido(models.Model):
    id = models.IntegerField(unique=True)
    

class Resultado(models.Model):
    goles_local = models.IntegerField(verbose_name="Goles local", null=False)
    goles_visitante = models.IntegerField(verbose_name="Goles visitante", null=False)

class DatosUsuario(models.Model):
    descripcion = models.TextField()
    POSICION = [
        ("GOA","Portero"),
        ("DEF","Defensa"),
        ("MID","Centrocampista"),
        ("STR", "Delantero")
    ]
    posicion = models.CharField(max_length=2, choices=POSICION)
    resultados = models.ForeignKey(Resultado)