from django.shortcuts import render
from .models import Usuario, Reserva, Partido, Post, Resultado
from django.db.models import Q, Prefetch, Count, F

# Create your views here.

#1. Crear un index que contenga todas las urls

def index(request):
    return render(request, "index.html")

#2. Mostrar datos de los usuarios

def usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_reserva"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_reserva__campo_reservado")).all()
    return render(request, "usuarios/lista.html", {"usuarios":QSusuarios})

#3. Mostrar usuarios de X posición

def buscar_usuario(request, pos):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_reserva"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_reserva__campo_reservado"))
    usuarios = QSusuarios.filter(datos_usuario__posicion__contains=pos).all()
    return render(request, "usuarios/usuario_posicion.html", {"usuarios":usuarios})

#4. Obtener las reservas realizadas de X usuario

def reservas_usuario(request, id_usuario):
    usuario_mostrar = Usuario.objects.get(id=id_usuario)
    QSreserva = Reserva.objects.select_related("creador").select_related("campo_reservado")
    reservas = QSreserva.filter(creador=id_usuario).all()
    return render(request, "reservas/reservas_usuarios.html", {"usuario":usuario_mostrar, "reservas":reservas})

#5. Mostrar los usuarios que pertenezcan a X partido (relación ManyToMany con tabla intermedia)

def usuarios_partido(request, id_partido):
    partido_mostrar = Partido.objects.get(id=id_partido)
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("jugadores_partido"))
    usuarios = QSusuarios.filter(jugador_partido__partido=id_partido).all()
    return render(request, "partidos/usuarios_partidos.html", {"partido":partido_mostrar, "usuarios":usuarios})

#6. DUDA. Mostrar los usuarios que hayan creado más de n posts

def usuarios_post(request, n):
    #QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_post"))
    #usuarios = QSusuarios.values("creador_post").annotate(creador_post__cantidad=Count("id"))
    QSposts = Post.objects.select_related("creador_post")
    cantidad_post = QSposts.values("creador_post").annotate(cantidad=Count("id"))
    posts = cantidad_post.filter(cantidad__gt = n).all()
    return render(request, "posts/posts_usuarios.html", {"posts": posts})

#7. Mostrar los resultados de los partidos que hayan ganado los visitantes

def ganados_visitantes(request):
    QSpartidos = Partido.objects.prefetch_related(Prefetch("resultado_partido"))
    partidos = QSpartidos.filter(resultado_partido__goles_visitante__gt = F("resultado_partido__goles_local")).all()
    return render(request, "resultados/ganados_visitantes.html", {"partidos":partidos})

#8. Mostrar los resultados de los partidos que hayan ganado los visitantes

def ganados_locales(request):
    QSpartidos = Partido.objects.prefetch_related(Prefetch("resultado_partido"))
    partidos = QSpartidos.filter(resultado_partido__goles_local__gt = F("resultado_partido__goles_visitante")).all()
    return render(request, "resultados/ganados_locales.html", {"partidos":partidos})

#9. Retorna todos los partidos que sean estilo futbol sala(5) o fútbol 7

def futbol_sala_siete(request):
    QSpartidos = Partido.objects.prefetch_related("usuarios_jugadores").select_related("reserva_partido")
    partidos = QSpartidos.filter(Q(estilo = 5) | Q(estilo = 7)).all()
    return render(request, "partidos/sala_o_siete.html", {"partidos":partidos})

#10. Muestra los datos de los 3 usuarios con más nivel

def niveles_usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("datos_usuario"),
                                                  Prefetch("jugadores_partido"))
    usuarios = QSusuarios.order_by("-nivel")[0:3].all()
    return render(request, "usuarios/niveles_usuarios.html", {"usuarios":usuarios})

# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)