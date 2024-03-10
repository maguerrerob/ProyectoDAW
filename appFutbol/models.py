from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    DUENYORECINTO = 3
    ROLES = (
        (ADMINISTRADOR, 'administardor'),
        (CLIENTE, 'cliente'),
        (DUENYORECINTO, 'duenyorecinto'),
    )

    rol  = models.PositiveSmallIntegerField(
        choices=ROLES,default=1
    )

    def __str__(self) -> str:
        return self.username


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    nivel = models.FloatField(default=0.0, db_column="puntos_usuario")
    telefono = models.CharField(max_length=9)

    def __str__(self):
        return self.usuario.username

class Duenyorecinto(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)
    telefono = models.CharField(max_length=9)


class Recinto(models.Model):
    nombre = models.TextField()
    ubicacion = models.TextField()
    telefono = models.CharField(max_length=9)
    latitud = models.FloatField(default=0)
    longitud =models.FloatField(default=0)
    duenyo_recinto = models.ForeignKey(Duenyorecinto, on_delete = models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class Partido(models.Model):
    hora = models.TimeField(default=timezone.now)
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
    ESTILO = [
        ("5", "Fútbol sala"),
        ("7", "Fútbol 7"),
        ("11", "Fútbol 11"),
    ]
    estilo = models.CharField(max_length=2, choices=ESTILO)
    #--------Relaciones--------
    creador = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="creador_partido")
    campo_reservado = models.ForeignKey(Recinto, on_delete=models.CASCADE, related_name="campo_reservadoo")
    usuarios_jugadores = models.ManyToManyField(Cliente, through="Jugador_partido", related_name="jugadores_partido")


class Jugador_partido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    ganar = models.BooleanField(default=False)


class Resultado(models.Model):
    goles_local = models.IntegerField(verbose_name="Goles local")
    goles_visitante = models.IntegerField(verbose_name="Goles visitante")
    #--------Relaciones--------
    resultado_partido = models.OneToOneField(Partido, on_delete=models.CASCADE, related_name="resultado_partido")


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
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name="datos_usuario")
    # Para ver los partidos en los que ha estado el usuario
    partidos_jugados = models.ManyToManyField(Partido)

    def __str__(self) -> str:
        return self.descripcion


class Post(models.Model):
    contenido = models.TextField()
    #--------Relaciones--------
    creador_post = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="creador_post")


class Votacion_partido(models.Model):
    puntuacion_numerica = models.IntegerField()
    comentario = models.TextField()
    fecha_votacion = models.DateTimeField(default=timezone.now)
    #--------Relaciones--------
    partido_votado = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name="votacion_partido")
    creador_votacion = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="votacion_usuario")


class Cuenta_bancaria(models.Model):
    numero_cuenta = models.IntegerField()
    BANCO = [
        ("CA", "Caixa"),
        ("BB", "BBVA"),
        ("UN", "Unicaja"),
        ("IN", "ING")
    ]
    banco = models.CharField(max_length=2, choices=BANCO)
    #--------Relaciones--------
    titular = models.OneToOneField(Cliente, on_delete=models.CASCADE, name="titular_cuenta")


# EXAMEN FORMULARIOS

class Promocion(models.Model):
    nombre = models.CharField(max_length=500)
    descripcion = models.TextField()
    descuento = models.IntegerField()
    fecha_promocion = models.DateField(default=timezone.now)
    #----Relaciones----
    miusuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nombre


class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_on.date()