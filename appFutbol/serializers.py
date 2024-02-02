from rest_framework import serializers
from .models import *
from datetime import datetime

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
                  "creadorPartido", "campo_reservado", "usuarios_jugadores"
                  ]
        
    def validate_hora(self,hora):
        libroHora = Partido.objects.filter(hora=hora).first()
        if(not libroHora is None):
            if(not self.instance is None and libroHora.id == self.instance.id):
                pass
            else:
                raise serializers.ValidationError('Ya existe un libro con ese hora')
        return hora
    
    def validate_hora_inicial(self,hora):
        hora_datetime = datetime.strptime(hora, "%H:%M")
        hora_siete_datetime = datetime.strptime("7:00", "%H:%M")
        if hora_datetime < hora_siete_datetime:
            raise serializers.ValidationError("Error, no puedes seleccionar esa hora")
        return hora
        
    def validate_campo_reservado(self,campo_reservado):
        if len(campo_reservado) < 1:
            raise serializers.ValidationError("Debe seleccionar al menos 1 campo")
        return campo_reservado
    
    # self.initial_data obtiene los datos sin serializar(string)