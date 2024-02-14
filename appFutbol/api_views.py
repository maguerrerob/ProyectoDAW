from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from rest_framework import status
from django.db.models import Q,Prefetch
from django.shortcuts import render,redirect
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
import os
from django.conf import settings
from django.http import HttpResponse


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

@api_view(['GET'])
def duenyosrecintos_list(request):
    duenyosrecintos = Dueñorecinto.objects.all()
    serializer = DuenyoRecintoSerializer(duenyosrecintos, many=True)
    return Response(serializer.data)


# Create Partido API
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
    
# Obtener un partido (para poder hacer PUT y PATCH)
@api_view(['GET'])
def partido_obtener(request,partido_id):
    partido = Partido.objects.select_related("creador", "campo_reservado")
    partido = partido.get(id=partido_id)
    serializer = PartidoSerializerMejorada(partido)
    return Response(serializer.data)
    
@api_view(['PUT'])
def partido_put(request,partido_id):
    partido = Partido.objects.get(id=partido_id)
    serializers = PartidoSerializerCreate(data=request.data,instance=partido)
    if serializers.is_valid():
        try:
            PartidoSerializerCreate.save()
            return Response("Partido EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(PartidoSerializerCreate.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def partido_eliminar(request, partido_id):
    partido = Partido.objects.get(id=partido_id)
    try:
        partido.delete()
        return Response("Partido eliminado")
    except Exception as error:
        return Response(error, status=status)


# CRUD Recinto API
@api_view(['POST'])
def recinto_create(request):
    serializers = RecintoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Recinto CREADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET']) 
def recinto_obtener(request,recinto_id):
    recinto = Recinto.objects.select_related("dueño_recinto")
    recinto = recinto.get(id=recinto_id)
    serializer = RecintoSerializer(recinto)
    return Response(serializer.data)

@api_view(['PUT'])
def recinto_put(request,recinto_id):
    recinto = Recinto.objects.get(id=recinto_id)
    serializers = RecintoSerializerCreate(data=request.data,instance=recinto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Recinto EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
def recinto_eliminar(request, recinto_id):
    datosusuario = Recinto.objects.get(id=recinto_id)
    try:
        datosusuario.delete()
        return Response("Recinto eliminado")
    except Exception as error:
        return Response(error, status=status)

    

# CRUD Datosusuario API
@api_view(['POST'])
def datosusuario_create(request):
    serializers = DatosUsuarioSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Datos usuario CREADO")
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def datosusuario_obtener(request,datosusuario_id):
    datosusuario = DatosUsuario.objects.select_related("cliente")
    datosusuario = datosusuario.get(id=datosusuario_id)
    serializer = DatosUsuariosSerializar(datosusuario)
    return Response(serializer.data)
    
@api_view(['PUT'])
def datosusuario_put(request,datosusuario_id):
    datosusuario = DatosUsuario.objects.get(id=datosusuario_id)
    serializers = DatosUsuarioSerializerCreate(data=request.data,instance=datosusuario)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Datos usuario EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def datosusuario_patch_ubicacion(request, datosusuario_id):
    datosusuario = DatosUsuario.objects.get(id=datosusuario_id)
    serializers = DatosUsuarioSerializerActualizarNombre(data=request.data,instance=datosusuario)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Ubicacion datos usuario EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def datosusuario_eliminar(request, datosusuario_id):
    datosusuario = DatosUsuario.objects.get(id=datosusuario_id)
    try:
        datosusuario.delete()
        return Response("Dato de usuario eliminado")
    except Exception as error:
        return Response(error, status=status)
    

# FileUpload
class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
# FileDownload
class FileDownload(APIView):
    def get(self, request, nombre_archivo):
        # Ruta al directorio de medios
        media_dir = settings.MEDIA_ROOT
        
        # Ruta al archivo solicitado
        ruta_archivo = os.path.join(media_dir, nombre_archivo)
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo) and nombre_archivo.lower().endswith('.txt'):
            # Abrir el archivo en modo de lectura binaria
            with open(ruta_archivo, 'rb') as archivo:
                # Leer el contenido del archivo
                contenido = archivo.read()
            
            # Crear una respuesta HTTP con el contenido del archivo
            response = Response(contenido, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
        if os.path.exists(ruta_archivo) and nombre_archivo.lower().endswith('.pdf'):
            # Abrir el archivo en modo de lectura binaria
            with open(ruta_archivo, 'rb') as archivo:
                # Leer el contenido del archivo
                contenido = archivo.read()
            
            # Crear una respuesta HTTP con el contenido del archivo
            response = HttpResponse(contenido, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
        else:
            # Si el archivo no existe, devolver una respuesta de error
            return Response("El archivo solicitado no existe", status=404)
        
class DeleteFile(APIView):
    def delete(self, request, nombre_archivo):
        # Ruta al directorio de medios
        media_dir = settings.MEDIA_ROOT

        # Ruta al archivo solicitado
        ruta_archivo = os.path.join(media_dir, nombre_archivo)

        # Verificar si el archivo existe
        if os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
                return Response({"mensaje": f"El archivo {nombre_archivo} ha sido eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"detalle": f"No se pudo eliminar el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detalle": "El archivo solicitado no existe"}, status=status.HTTP_404_NOT_FOUND)