from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from rest_framework import status
from django.db.models import Q,Prefetch

@api_view(["GET"])
def partido_list(request):
    partidos = Partido.objects.all()
    serializer = PartidoSerializer(partidos, many=True)
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