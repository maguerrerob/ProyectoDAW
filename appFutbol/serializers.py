from rest_framework import serializers
from .models import *

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

class RecintoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = "__all__"

         
class JugadorPartidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer()
    
    class Meta:
        model = Jugador_partido
        fields = "__all__"
        

class PartidoSerializer(serializers.ModelSerializer):
    # Para la relación Many To One con Recinto
    campo_reservado = RecintoSerializer()
    
    # Para la relación Many to One con Cliente
    creador = ClienteSerializer()
    
    # Para la relacion Many To One con 
    usuarios_jugadores = JugadorPartidoSerializer(read_only=True, source="jugador_partido_set",many=True)
    
    # Para los choices
    estado = serializers.CharField(source="get_estado_display")
    tipo = serializers.CharField(source="get_tipo_display")
    estilo = serializers.CharField(source="get_estilo_display")
    
    class Meta:
        model = Partido
        fields = "__all__"


