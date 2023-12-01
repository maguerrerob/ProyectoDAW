from django.shortcuts import render, redirect
from .models import Usuario, Reserva, Partido, Post, Resultado, Votacion_partido, Cuenta_bancaria
from django.db.models import Q, Prefetch, Count, F,Avg
from .forms import *

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
    partidos = (QSpartidos.filter(Q(estilo = 5) | Q(estilo = 7))).filter(reserva_partido__estado="A").all()
    return render(request, "partidos/sala_o_siete.html", {"partidos":partidos})

#10. Muestra los datos de los 3 usuarios con más nivel

def niveles_usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("datos_usuario"),
                                                  Prefetch("jugadores_partido"))
    usuarios = QSusuarios.order_by("-nivel")[0:3].all()
    return render(request, "usuarios/niveles_usuarios.html", {"usuarios":usuarios})

def reservas_realizadas(request):
    QSreservas = Reserva.objects.select_related("creador", "campo_reservado")
    reservas = QSreservas.all()
    return render(request, "reservas/lista_reservas.html", {"reservas":reservas})

#1.E El último voto que se realizó en un modelo principal en concreto, y mostrar el comentario, la votación e información del usuario o cliente que lo realizó.

def ultima_votacion(request, id_partido):
    tarea_mostrar = Partido.objects.get(id=id_partido)
    QSvotaciones = Votacion_partido.objects.select_related("creador_votacion")
    votacion = QSvotaciones.filter(partido_votado=id_partido)[0:1].get()
    return render(request, "votaciones/ultima_votacion.html", {"tarea":tarea_mostrar,"votacion":votacion})

#2.E Todos los modelos principales que tengan votos con una puntuación numérica igual a 3 y que realizó un usuario o cliente en concreto.

def votacion_3(request,id_usuario):
    usuario_mostrar = Usuario.objects.get(id=id_usuario)
    QSpartidos = Partido.objects.select_related("reserva_partido").prefetch_related("usuarios_jugadores")
    partidos = (QSpartidos.filter(votacion_partido__puntuacion_numerica=3)).filter(votacion_partido__creador_votacion=id_usuario)
    return render(request, "votaciones/votacion_3.html", {"usuario":usuario_mostrar, "partidos":partidos})

#3.E Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo.

def usuarios_sin_votaciones(request):
    QSvotaciones = Votacion_partido.objects.select_related("creador_votacion")
    votaciones = QSvotaciones.filter(creador_votacion=None).all()
    return render(request, "votaciones/usuarios_sin_votar.html", {"votaciones":votaciones})
    
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_post"))
    usuarios = QSusuarios.exclude(votacion_usuario__creador_votacion=None).all()
    #usuarios = QSusuarios.filter(votacion_usuario__creador_votacion__ne=id)
    return render(request, "votaciones/usuarios_sin_votar.html", {"usuarios":usuarios})

#4.E Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”.

def validar_banco(request, nombre):
    QScuentas = Cuenta_bancaria.objects.select_related("titular_cuenta")
    cuentas = (QScuentas.filter(Q(banco="CA") | Q(banco="UN"))).filter(titular_cuenta__nombre__contains=nombre).all()
    return render(request, "votaciones/datos_bancos.html", {"cuentas":cuentas})

#5.E Obtener todos los modelos principales que tengan una media de votaciones mayor del 2,5.

def media_partidos(request):
    QSvotaciones = Votacion_partido.objects.select_related("partido_votado")
    votaciones = QSvotaciones.aggregate(media=Avg('puntuacion_numerica'))
    mayores  = Votacion_partido.objects.filter(puntuacion_numerica__gt=2.5)
    return render(request, "votaciones/media_votaciones.html", {"mayores":mayores})

# FORMULARIOS

def reserva_create(request):
    if request.method == "POST":
        formulario = ReservaModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guardamos la reserva en la base de datos
                formulario.save()
                return redirect("reservas_realizadas")
            except Exception as error:
                print(error)
    else:
        formulario = ReservaModelForm()
    
    return render(request, "reservas/create.html", {"formulario":formulario})

def reserva_buscar(request):
    formulario = BusquedaReservaForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get("textoBusqueda")
        QSreservas = Reserva.objects.select_related("creador", "campo_reservado")
        reservas = QSreservas.filter(creador__nombre__contains=texto).all()
        mensaje_busqueda = "Reservas realizadas por el usuario: " + texto
        return render(request, "reservas/lista_busqueda.html", {"reservas":reservas, "texto_bsuqueda":mensaje_busqueda})

    if ("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)