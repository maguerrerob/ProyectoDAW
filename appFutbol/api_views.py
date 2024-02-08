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
    if (request.user.has_perm("appFutbol.view_partido")):
        partidos = Partido.objects.all()
        serializer = PartidoSerializer(partidos, many=True)
        return Response(serializer.data)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)

# Consulta mejorada
@api_view(["GET"])
def partido_list_mejorada(request):
    if (request.user.has_perm("appFutbol.view_partido")):
        partidos = Partido.objects.all()
        serializer = PartidoSerializerMejorada(partidos, many=True)
        return Response(serializer.data)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)

# Consultas mejoradas con oauth2
@api_view(['GET'])
def datosusuarios_list(request):
    if (request.user.has_perm("appFutbol.view_datosusuario")):
        datosuaurios = DatosUsuario.objects.all()
        serializer = DatosUsuariosSerializar(datosuaurios, many=True)
        return Response(serializer.data)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def recintos_list(request):
    recintos = Recinto.objects.all()
    serializer = RecintoSerializer(recintos, many=True)
    return Response(serializer.data)

# Consulta con JWT
@api_view(["GET"])
def posts_listar(request):
    if (request.user.has_perm("appFutbol.view_post")):
        posts = Post.objects.all()
        serializer = Postsserializer(posts, many=True)
        return Response(serializer.data)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def recinto_busqueda_simple(request):
    if (request.user.has_perm("appFutbol.view_recinto")):
        formulario = BusquedaRecintoForm(request.query_params)
        if(formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            QSrecintos = Recinto.objects.select_related("dueño_recinto")
            recintos = QSrecintos.filter(Q(nombre__contains=texto) | Q(ubicacion__contains=texto)).all()
            serializer = RecintoSerializer(recintos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("Sin permisooooos")
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def recinto_buscar_avanzado(request):
    if (request.user.has_perm("appFutbol.view_recinto")):
        if(len(request.query_params) > 0):
            formulario = BusquedaAvanzadaRecintoFormGen(request.GET)
            if formulario.is_valid():

                #Obtenemos los filtros
                nombre = formulario.cleaned_data.get("nombre")
                ubicacion = formulario.cleaned_data.get("ubicacion")
                telefono = formulario.cleaned_data.get("telefono")

                QSrecinto = Recinto.objects.all()
                
                if(nombre != ""):
                    QSrecinto = QSrecinto.filter(nombre__contains=nombre)
                    print("se metioooooooooooooooooooo")
                if (ubicacion != ""):
                    QSrecinto = QSrecinto.filter(ubicacion__contains=ubicacion)
                if (telefono != ""):
                    QSrecinto = QSrecinto.filter(telefono__contains=telefono)
                    
                recintos = QSrecinto.all()
                
                serializer = RecintoSerializer(recintos, many=True)

                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("Sin permisooooos")
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def datosusuario_busqueda_avanzada(request):
    if (request.user.has_perm("appFutbol.view_datosusuario")):
        if(len(request.query_params) > 0):
            formulario = BusquedaAvanzadaDatosusuarioFormGen(request.GET)
            if formulario.is_valid():

                #Obtenemos los filtros
                descripcion = formulario.cleaned_data.get("descripcion")
                posicion = formulario.cleaned_data.get("posicion")
                ubicacion = formulario.cleaned_data.get("ubicacion")

                QSdatosusuario = DatosUsuario.objects.all()

                if(descripcion != ""):
                    QSdatosusuario = QSdatosusuario.filter(descripcion__contains=descripcion)

                if (ubicacion != ""):
                    QSdatosusuario = QSdatosusuario.filter(ubicacion__contains=ubicacion)
                
                if(len(posicion) > 0):
                    filtroOR = Q(posicion=posicion[0])
                    for pos in posicion[1:]:
                        filtroOR |= Q(posicion=pos)
                    
                    QSdatosusuario =  QSdatosusuario.filter(filtroOR)

                datosusuarios = QSdatosusuario.all()
                
                serializer = DatosUsuariosSerializar(datosusuarios, many=True)

                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def partido_buscar_avanzado(request):
    if (request.user.has_perm("appFutbol.view_partido")):
        if(len(request.query_params) > 0):
            formulario = BusquedaAvanzadaPartidoForm(request.query_params)
            if formulario.is_valid():
                QSpartido = Partido.objects.select_related("creador", "campo_reservado").prefetch_related("usuarios_jugadores")

                #Obtenemos los filtros
                estado = formulario.cleaned_data.get("estado")
                estilo = formulario.cleaned_data.get("estilo")

                if (not estado is None):
                    QSpartido = QSpartido.filter(estado=estado)

                if(len(estilo) > 0):
                    filtroOR = Q(estilo=estilo[0])
                    for est in estilo[1:]:
                        filtroOR |= Q(estilo=est)
                    QSpartido =  QSpartido.filter(filtroOR)
                
                partidos = QSpartido.all()
                serializer = PartidoSerializerMejorada(partidos, many=True)
                return Response(serializer.data)
            else:
                return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)

    

# Listar clientes
@api_view(['GET'])
def clientes_list(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

# Create partido API
@api_view(['POST'])
def partido_create(request):
    serializers = PartidoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Partido CREADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)