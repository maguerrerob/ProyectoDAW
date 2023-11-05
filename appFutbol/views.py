from django.shortcuts import render
from .models import Usuario
from django.db.models import Q, Prefetch

# Create your views here.

def index(request):
    return render(request, "index.html")


#1. Mostrar datos de los usuarios

def usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_reserva"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_reserva__campo_reservado")).all()
    return render(request, "usuarios/lista.html", {"usuarios":QSusuarios})

#2. Mostrar usuarios de X posición

def buscar_usuario(request, pos):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_reserva"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_reserva__campo_reservado"))
    usuarios = QSusuarios.filter(datos_usuario__posicion__contains=pos).all()
    return render(request, "usuarios/usuario_posicion.html", {"usuarios":usuarios})

#3. Mostrar los usuarios que hayan creado más X posts

def usuarios_post(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_reserva"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_reserva__campo_reservado"))
    #usuarios = QSusuarios.filter(datos_usuario__)