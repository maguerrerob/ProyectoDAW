from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(["GET"])
def partido_list(request):
    partidos = Partido.objects.all()
    serializer = PartidoSerializer(partidos, many=True)
    return Response(serializer.data)