from rest_framework import serializers
from .models import *
from datetime import datetime
from datetime import time
from .models import UploadedFile

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class ClienteSerializer(serializers.ModelSerializer):
    # Para la relación One To One con Usuario
    usuario = UsuarioSerializer()

    class Meta:
        model = Cliente
        fields = "__all__"

class DuenyoRecintoSerializer(serializers.ModelSerializer):
    # Para la relación One To One con Usuario
    usuario = UsuarioSerializer()

    class Meta:
        model = Duenyorecinto
        fields = "__all__"

class RecintoSerializer(serializers.ModelSerializer):
    duenyo_recinto = DuenyoRecintoSerializer()

    class Meta:
        model = Recinto
        fields = "__all__"

class Postsserializer(serializers.ModelSerializer):
    creador_post = ClienteSerializer()

    class Meta:
        model = Post
        fields = "__all__"


class JugadorPartidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()

    class Meta:
        model = Jugador_partido
        fields = "__all__"


class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = "__all__"

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = "__all__"

class PartidoSerializerMejorada(serializers.ModelSerializer):
    # Para la relación Many To One con Recinto
    campo_reservado = RecintoSerializer()

    # Para la relación Many to One con Cliente
    creador = ClienteSerializer()

    # Relación OneToOne con Resultado
    resultado_partido = ResultadoSerializer()

    # Para la relacion Many To One con jugador_partido (tabla intermedia)
    usuarios_jugadores = JugadorPartidoSerializer(read_only=True, source="jugador_partido_set",many=True)

    # Para los choices
    estado = serializers.CharField(source="get_estado_display")
    tipo = serializers.CharField(source="get_tipo_display")
    estilo = serializers.CharField(source="get_estilo_display")

    class Meta:
        model = Partido
        fields = "__all__"

class DatosUsuariosSerializar(serializers.ModelSerializer):
    cliente = ClienteSerializer()

    posicion = serializers.CharField(source="get_posicion_display")
    class Meta:
        model = DatosUsuario
        fields = "__all__"


# Serializer del formulario create partidos
class PartidoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = ["hora", "estado",
                  "tipo", "estilo",
                  "creador", "campo_reservado"
                  ]

    def validate_hora(self,hora):
        hora_reserva = self.initial_data["hora"]
        hora_datetime = datetime.strptime(hora_reserva, "%H:%M:%S")
        hora_siete_datetime = datetime.strptime("7:00:00", "%H:%M:%S")
        print(type(hora_siete_datetime))
        print(hora_datetime)
        if hora_datetime < hora_siete_datetime:
            raise serializers.ValidationError("Error, no puedes seleccionar esa hora")
        return hora

    def validate_campo_reservado(self,campo_reservado):
        horareserva = self.initial_data["hora"]
        hora_datetime = datetime.strptime(horareserva, "%H:%M:%S")
        print(type(hora_datetime))
        QScampoReservado = Partido.objects.filter(campo_reservado=campo_reservado).filter(hora=hora_datetime).first()
        print(QScampoReservado)
        if (QScampoReservado is not None):
            raise serializers.ValidationError('Ya existe una reserva a esa hora en ese campo')

        return campo_reservado


    # self.initial_data obtiene los datos sin serializar(string)

class PartidoSerializerActualizarHora(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = ["hora"] #campo_reservado

    def validate_hora(self,hora):
        # campo_reservado = self.initial_data["campo_reservado"]
        # QSocupado = Partido.objects.filter(hora=hora).filter(campo_reservado=campo_reservado).first()
        # if (QSocupado is not None):
        #     raise serializers.ValidationError("No puedes cambiar a esa hora, ya está reservado")
        print(type(hora))
        hora_reserva = self.initial_data["hora"]
        print(type(hora_reserva))
        hora_datetime = datetime.strptime(hora_reserva, "%H:%M:%S")
        print(type(hora_datetime))
        hora_siete_datetime = datetime.strptime("7:00:00", "%H:%M:%S")

        if hora_datetime < hora_siete_datetime:
            raise serializers.ValidationError("Error, no puedes seleccionar una hora antes de las 7:00:00")
        return hora

class RecintoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = [
            "nombre", "ubicacion",
            "telefono", "duenyo_recinto",
            "latitud", "longitud"
        ]

    def validate_telefono(self, telefono):
        if len(telefono) < 9:
            raise serializers.ValidationError("Error, el teléfono debe tener min 9 numeros")

        return telefono

class RecintoSerializerActualizarNombre(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = ["nombre"]

    def validate_nombre(self, nombre):
        QSnombre = Recinto.objects.filter(nombre=nombre).first()
        if (QSnombre is not None):
            raise serializers.ValidationError("Error, ese nombre de recinto ya existe en la BD")
        return nombre

class DatosUsuarioSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = DatosUsuario
        fields = [
            "descripcion", "posicion",
            "ubicacion", "cliente"
        ]

    def validate_descripcion(self, descripcion):
        if len(descripcion) > 150:
            raise serializers.ValidationError("Error, la descripcion pasa de los 150 carácteres")

        return descripcion

    def validate_posicion(self, posicion):
        print("posicionnnnnnnnnnnn")
        print(posicion)
        print(type(posicion))
        print(self.initial_data["posicion"])
        # Pongo mayor de 3 porque posición devuelve la clave del diccionario posición (DEF o STR, etc)
        if len(posicion) > 3:
            raise serializers.ValidationError("Error, no puedes tener más de 3 posiciones")

        return posicion

    def validate_ubicacion(self, ubicacion):
        if len(ubicacion) > 80:
            raise serializers.ValidationError("Error, ubicación con más de 80 carácteres")

        return ubicacion

class DatosUsuarioSerializerActualizarUbicacion(serializers.ModelSerializer):
    class Meta:
        model = DatosUsuario
        fields = ['ubicacion']

    def validate_ubicacion(self,ubicacion):
        if len(ubicacion) > 200:
            raise serializers.ValidationError("Error, esa ubicación es muy extensa")
        return ubicacion


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)


#----Registro----
class UsuarioSerializerRegistro(serializers.Serializer):

    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField()
    rol = serializers.IntegerField()

    def validate_username(self,username):
        usuario = Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError('Ya existe un usuario con ese nombre')
        return username

class JugadorPartidoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Jugador_partido
        fields = ["cliente", "partido"]

class ResultadoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = ["goles_local", "goles_visitante",
                  "resultado_partido"]