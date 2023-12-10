from django.conf import settings
from django.db import models
from django.utils import timezone
from automatic_crud.models import BaseModel

# Create your models here.

class Usuario(BaseModel):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    nivel = models.FloatField(default=0.0, db_column="puntos_usuario")
    telefono = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.nombre


class Recinto(BaseModel):
    nombre = models.TextField()
    ubicacion = models.TextField()
    telefono = models.CharField(max_length=9)
    
    def __str__(self) -> str:
        return self.nombre


class Partido(BaseModel):
    ESTADO = [
        ("F", "Completo"),
        ("A", "Disponible")
    ]
    estado = models.CharField(max_length=1, default="A" ,choices=ESTADO)
    TIPO = [
        ("Pr", "Privada"),
        ("Pu", "Pública")
    ]
    tipo = models.CharField(max_length=2, choices=TIPO)
    # Campo para manejar con IF si un partido está completa o no dependiendo del estilo de juego
    ESTILO = [
        ("5", "Fútbol sala"),
        ("7", "Fútbol 7"),
        ("11", "Fútbol 11"),
    ]
    estilo = models.CharField(max_length=2, choices=ESTILO)
    #--------Relaciones--------
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="creador_partido")
    campo_reservado = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    usuarios_jugadores = models.ManyToManyField(Usuario, through="Jugador_partido", related_name="jugadores_partido")


class Jugador_partido(BaseModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    ganar = models.BooleanField(default=False)


class Resultado(BaseModel):
    goles_local = models.IntegerField(verbose_name="Goles local")
    goles_visitante = models.IntegerField(verbose_name="Goles visitante")
    #--------Relaciones--------
    resultado_partido = models.OneToOneField(Partido, on_delete=models.CASCADE, related_name="resultado_partido")


class DatosUsuario(BaseModel):
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
    # Para ver los partidos en los que ha estado el usuario
    partidos_jugados = models.ManyToManyField(Partido)


class Post(BaseModel):
    contenido = models.TextField()
    #--------Relaciones--------
    creador_post = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="creador_post")


class Votacion_partido(BaseModel):
    puntuacion_numerica = models.IntegerField()
    comentario = models.TextField()
    fecha_votacion = models.DateTimeField(default=timezone.now)
    #--------Relaciones--------
    partido_votado = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name="votacion_partido")
    creador_votacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="votacion_usuario")
    

class Cuenta_bancaria(BaseModel):
    numero_cuenta = models.IntegerField()
    BANCO = [
        ("CA", "Caixa"),
        ("BB", "BBVA"),
        ("UN", "Unicaja"),
        ("IN", "ING")
    ]
    banco = models.CharField(max_length=2, choices=BANCO)
    #--------Relaciones--------
    titular = models.OneToOneField(Usuario, on_delete=models.CASCADE, name="titular_cuenta")