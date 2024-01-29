from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from rest_framework import status
from django.db.models import Q,Prefetch
from django.shortcuts import render,redirect

# Consulta sencilla a modelo principal
@api_view(["GET"])
def partido_list(request):
    partidos = Partido.objects.all()
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)

# Consulta mejorada
@api_view(["GET"])
def partido_list_mejorada(request):
    partidos = Partido.objects.all()
    serializer = PartidoSerializerMejorada(partidos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def recintos_list(request):
    recintos = Recinto.objects.all()
    serializer = RecintoSerializer(recintos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def recinto_busqueda_simple(request):
    formulario = BusquedaRecintoForm(request.query_params)
    if(formulario.is_valid()):
        texto = formulario.data.get('textoBusqueda')
        QSrecintos = Recinto.objects.select_related("dueño_recinto")
        recintos = QSrecintos.filter(Q(nombre__contains=texto) | Q(ubicacion__contains=texto)).all()
        serializer = RecintoSerializer(recintos, many=True)
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def recinto_buscar_avanzado(request):
    if(len(request.query_params) > 0):
        formulario = BusquedaAvanzadaRecintoFormGen(request.GET)
        if formulario.is_valid():
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            #Obtenemos los filtros
            nombre = formulario.cleaned_data.get("nombre")
            ubicacion = formulario.cleaned_data.get("ubicacion")
            telefono = formulario.cleaned_data.get("telefono")

            if(nombre != ""
               and telefono != ""
               and ubicacion != ""):
                QSrecinto = Recinto.objects.filter(Q(nombre__contains=nombre) | Q(telefono=telefono) | Q(ubicacion=ubicacion))
                mensaje_busqueda += "Nombre que contenga: " + nombre + ", ubicación que corresponda a " + ubicacion + " y teléfono: " + telefono + "\n"

            recintos = QSrecinto.all()
            
            serializer = RecintoSerializer(recintos, many=True)

            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def datosusuarios_list(request):
    datosuaurios = DatosUsuario.objects.all()
    serializer = DatosUsuariosSerializar(datosuaurios, many=True)
    return Response(serializer.data)