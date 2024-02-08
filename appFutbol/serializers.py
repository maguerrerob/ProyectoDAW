from rest_framework import serializers
from .models import *
from datetime import datetime
from datetime import time

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
        model = Dueñorecinto
        fields = "__all__"

class RecintoSerializer(serializers.ModelSerializer):
    dueño_recinto = DuenyoRecintoSerializer()
    
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

class PartidoSerializerMejorada(serializers.ModelSerializer):
    # Para la relación Many To One con Recinto
    campo_reservado = RecintoSerializer()
    
    # Para la relación Many to One con Cliente
    creador = ClienteSerializer()
    
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
                  "creador", "campo_reservado", "usuarios_jugadores"
                  ]
        
    def validate_hora(self,hora):
        hora_reserva = self.initial_data["hora"]
        hora_datetime = datetime.strptime(hora_reserva, "%H:%M")
        hora_siete_datetime = datetime.strptime("7:00", "%H:%M")
        print(type(hora_siete_datetime))
        print(hora_datetime)
        if hora_datetime < hora_siete_datetime:
            raise serializers.ValidationError("Error, no puedes seleccionar esa hora")
        return hora

    def validate_campo_reservado(self,campo_reservado):
        horareserva = self.initial_data["hora"]
        hora_datetime = datetime.strptime(horareserva, "%H:%M")
        print(type(hora_datetime))
        QScampoReservado = Partido.objects.filter(campo_reservado=campo_reservado).filter(hora=hora_datetime).first()
        print(QScampoReservado)
        if (QScampoReservado is not None):
            raise serializers.ValidationError('Ya existe una reserva a esa hora en ese campo')

        return campo_reservado
        
    
    # self.initial_data obtiene los datos sin serializar(string)