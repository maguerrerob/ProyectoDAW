from django.shortcuts import render, redirect
from .models import Usuario, Recinto, Partido, Jugador_partido, Resultado, DatosUsuario, Post, Votacion_partido, Cuenta_bancaria, Promocion
from django.db.models import Q, Prefetch, Count, F,Avg
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

# Create your views here.

#1. Crear un index que contenga todas las urls

def index(request):
    return render(request, "index.html", {"usuario":request.user})

#2. Mostrar datos de los usuarios

def usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_partido"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_partido__campo_reservado")).all()
    return render(request, "usuarios/lista.html", {"usuarios":QSusuarios})

#3. Mostrar usuarios de X posición

def buscar_usuario(request, pos):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("creador_partido"),
                                                  Prefetch("datos_usuario"), 
                                                  Prefetch("creador_post"),
                                                  Prefetch("creador_partido__campo_reservado"))
    usuarios = QSusuarios.filter(datos_usuario__posicion__contains=pos).all()
    return render(request, "usuarios/usuario_posicion.html", {"usuarios":usuarios})

#4. Obtener las partidos creados de X usuario

def partidos_usuario(request, id_usuario):
    usuario_mostrar = Usuario.objects.get(id=id_usuario)
    QSpartido = Partido.objects.select_related("creador").select_related("campo_reservado")
    partidos = QSpartido.filter(creador=id_usuario).all()
    return render(request, "partidos/partidos_usuarios.html", {"usuario":usuario_mostrar, "partido":partidos})

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

#9. Retorna todos los partidos disponibles que sean estilo futbol sala(5) o fútbol 7

def futbol_sala_siete(request):
    QSpartidos = Partido.objects.select_related("creador", "campo_reservado").prefetch_related("usuarios_jugadores")
    partidos = (QSpartidos.filter(Q(estilo = 5) | Q(estilo = 7))).filter(estado="A").all()
    return render(request, "partidos/sala_o_siete.html", {"partidos":partidos})

#10. Muestra los datos de los 3 usuarios con más nivel

def niveles_usuarios(request):
    QSusuarios = Usuario.objects.prefetch_related(Prefetch("datos_usuario"),
                                                  Prefetch("jugadores_partido"))
    usuarios = QSusuarios.order_by("-nivel")[0:3].all()
    return render(request, "usuarios/niveles_usuarios.html", {"usuarios":usuarios})


#1.E El último voto que se realizó en un modelo principal en concreto, y mostrar el comentario, la votación e información del usuario o cliente que lo realizó.

def ultima_votacion(request, id_partido):
    tarea_mostrar = Partido.objects.get(id=id_partido)
    QSvotaciones = Votacion_partido.objects.select_related("creador_votacion")
    votacion = QSvotaciones.filter(partido_votado=id_partido)[0:1].get()
    return render(request, "votaciones/ultima_votacion.html", {"tarea":tarea_mostrar,"votacion":votacion})

#2.E Todos los modelos principales que tengan votos con una puntuación numérica igual a 3 y que realizó un usuario o cliente en concreto.

def votacion_3(request,id_usuario):
    usuario_mostrar = Usuario.objects.get(id=id_usuario)
    QSpartidos = Partido.objects.select_related("creador", "campo_reservado").prefetch_related("usuarios_jugadores")
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

# Usuario - CRUD
def usuarios_creados(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuarios/listado_usuarios.html",  {"usuarios":usuarios})


#def usuarios_create(request):
    if request.method == "POST":
        formulario = UsuarioModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guardamos el partido en la base de datos
                formulario.save()
                return redirect("usuarios_creados")
            except Exception as error:
                print(error)
    else:
        formulario = UsuarioModelForm()
    
    return render(request, "usuarios/create.html", {"formulario":formulario})


def usuario_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            #Obtenemos los filtros

            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            nivel = formulario.cleaned_data.get("nivel")

            if(textoBusqueda != ""):
                QSUsuario = Usuario.objects.filter(Q(nombre__contains=textoBusqueda) | Q(apellidos__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o apellido que contengan los datos " + textoBusqueda+"\n"

            if (nivel != 0,0):
                QSUsuario = QSUsuario.filter(nivel__gte=nivel)
                mensaje_busqueda +=" y su nivel sea igual o mayor de " + str(nivel)+"\n"
            
            usuarios = QSUsuario.all()

            return render(request, "usuarios/listado_usuarios.html", {"usuarios":usuarios, "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaUsuarioForm(None)
        
    return render(request, "usuarios/busqueda_avanzada.html", {"formulario":formulario})


#def usuario_editar(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    formulario = UsuarioModelForm(datosFormulario,instance = usuario)

    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("usuarios_creados")
            except Exception as error:
                pass

    return render(request, "usuarios/actualizar.html", {"formulario":formulario, "usuario":usuario})


#def usuario_eliminar(request,usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    try:
        usuario.delete()
        messages.success(request, "Se ha elimnado el usuario " + usuario.nombre + " correctamente")
    except Exception as error:
        print(error)
    return redirect('usuarios_creados')


def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if(rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='cliente') 
                grupo.user_set.add(user)
                cliente = Cliente.objects.create( usuario = user)
                cliente.save()
            elif(rol == Usuario.DUEÑORECINTO):
                grupo = Group.objects.get(name='dueñorecinto') 
                grupo.user_set.add(user)
                dueñorecinto = Dueñorecinto.objects.create(usuario = user)
                dueñorecinto.save()
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})


# Partido - CRUD
def partidos_realizados(request):
    QSpartidos = Partido.objects.select_related("creador", "campo_reservado").prefetch_related("usuarios_jugadores")
    partidos = QSpartidos.all()
    return render(request, "partidos/listado_partidos.html", {"partidos":partidos})

@permission_required("appFutbol.add_partido")
def partido_create(request):
    if request.method == "POST":
        formulario = PartidoModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guardamos el partido en la base de datos
                formulario.save()
                return redirect("partidos_realizados")
            except Exception as error:
                print(error)
    else:
        formulario = PartidoModelForm(initial={"creador":request.user.cliente})
    
    return render(request, "partidos/create.html", {"formulario":formulario})

@permission_required("appFutbol.view_partido")
def partido_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPartidoForm(request.GET)
        
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSpartido = Partido.objects.select_related("creador", "campo_reservado").prefetch_related("usuarios_jugadores")

            #Obtenemos los filtros

            estado_form = formulario.cleaned_data.get("estado_form")
            estilos_form = formulario.cleaned_data.get("estilos_form")


            if (not estado_form is None):
                mensaje_busqueda += "El estado sea: " + estado_form + "\n"
                QSpartido = QSpartido.filter(estado=estado_form)

            if(len(estilos_form) > 0):
                mensaje_busqueda +=" El estilo sea " + estilos_form[0]
                filtroOR = Q(estilo = estilos_form[0])
                for est in estilos_form[1:]:
                    mensaje_busqueda += " o " + estilos_form[1]
                    filtroOR |= Q(estilo = est)
                mensaje_busqueda += "\n"
                QSpartido =  QSpartido.filter(filtroOR)
            
            partidos = QSpartido.all()

            return render(request, "partidos/listado_partidos.html", {"partidos":partidos, "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaPartidoForm(None)
        
    return render(request, "partidos/busqueda_avanzada.html", {"formulario":formulario})

@permission_required("appFutbol.change_partido")
def partido_editar(request, partido_id):
    partido = Partido.objects.get(id=partido_id)
    
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    formulario = PartidoModelForm(datosFormulario,instance = partido)

    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("partidos_realizados")
            except Exception as error:
                pass

    return render(request, "partidos/actualizar.html", {"formulario":formulario, "partido":partido})

@permission_required("appFutbol.delete_partido")
def partido_eliminar(request,partido_id):
    partido = Partido.objects.get(id=partido_id)
    try:
        partido.delete()
        messages.success(request, "Se ha elimnado el partido de estilo " + partido.estilo + " correctamente")
    except Exception as error:
        print(error)
    return redirect('partidos_realizados')


# Recinto - CRUD
def listar_recintos(request):
    recintos = Recinto.objects.all()
    return render(request, "recintos/listado_recintos.html", {"recintos":recintos})


@permission_required("appFutbol.add_recinto")
def recinto_create(request):
    if request.method == "POST":
        formulario = RecintoModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guardamos el partido en la base de datos
                formulario.save()
                return redirect("listar_recintos")
            except Exception as error:
                print(error)
    else:
        formulario = RecintoModelForm(initial={"dueño_recinto":request.user.dueñorecinto})
    
    return render(request, "recintos/create.html", {"formulario":formulario})


# Uso el mismo template de "listado_recintos.html" y pongo un if si llega un mensaje_busqueda ya que son el mismo template sin eso.
def recinto_buscar(request):
    formulario = BusquedaRecintoForm(request.GET)
    
    if formulario.is_valid():
        texto = formulario.cleaned_data.get("textoBusqueda")
        recintos = Recinto.objects.filter(ubicacion__contains=texto).all()
        mensaje_busqueda = "Recintos con ubicación: " + texto
        return render(request, "recintos/listado_recintos.html", {"recintos":recintos, "texto_busqueda":mensaje_busqueda})

    if ("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")


def recinto_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaRecintoForm(request.GET)
        
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            #Obtenemos los filtros
            nombre = formulario.cleaned_data.get("nombre")
            telefono = formulario.cleaned_data.get("telefono")

            if(nombre != ""
               and telefono != ""):
                QSrecinto = Recinto.objects.filter(Q(nombre__contains=nombre) | Q(telefono=telefono))
                mensaje_busqueda += "Nombre que contenga: " + nombre + " y teléfono que corresponda a " + telefono +"\n"
            
            recintos = QSrecinto.all()

            return render(request, "recintos/listado_recintos.html", {"recintos":recintos, "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaRecintoForm(None)
        
    return render(request, "recintos/busqueda_avanzada.html", {"formulario":formulario})


@permission_required("appFutbol.change_recinto")
def recinto_editar(request, recinto_id):
    recinto = Recinto.objects.get(id=recinto_id)
    
    datosFormulario = None

    if request.method == "POST":
        datosFormulario = request.POST

    formulario = RecintoModelForm(datosFormulario,instance = recinto)

    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("listar_recintos")
            except Exception as error:
                pass

    return render(request, "recintos/actualizar.html", {"formulario":formulario, "recinto":recinto})


@permission_required("appFutbol.delete_recinto")
def recinto_eliminar(request,recinto_id):
    recinto = Recinto.objects.get(id=recinto_id)
    try:
        recinto.delete()
        messages.success(request, "Se ha elimnado el recinto " + recinto.nombre + " correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_recintos')


# Resultado - CRUD
def resultado_create(request):
    if request.method == "POST":
        formulario = ResultadoModelForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("partidos_realizados")
            except Exception as error:
                print(error)
    else:
        formulario = ResultadoModelForm()
    
    return render(request, "resultados/create.html", {"formulario":formulario})


def resultado_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaResultadoForm(request.GET)
        
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"

            #Obtenemos los filtros
            goles_local = formulario.cleaned_data.get("goles_local")
            goles_visitante = formulario.cleaned_data.get("goles_visitante")

            if(goles_local != ""
               and goles_visitante != ""):
                QSrecinto = Resultado.objects.filter(Q(goles_local__gte=1) | Q(telefono=telefono))
                mensaje_busqueda += "Nombre que contenga: " + nombre + " y teléfono que corresponda a " + telefono +"\n"
            
            recintos = QSrecinto.all()

            return render(request, "recintos/listado_recintos.html", {"recintos":recintos, "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaRecintoForm(None)
        
    return render(request, "recintos/busqueda_avanzada.html", {"formulario":formulario})


# VISTAS EXAMEN_FORMULARIOS

def promociones_realizadas(request):
    QSpromociones = Promocion.objects.select_related("miusuario")
    promociones = QSpromociones.all()
    return render(request, "promocion/listado_promociones.html", {"promociones":promociones})

def promocion_create(request):
    if request.method == "POST":
        formulario = PromocionModelForm(request.POST)
        if formulario.is_valid():
            try:
                # Guardamos el partido en la base de datos
                formulario.save()
                # Name de vista
                return redirect("promociones_realizadas")
            except Exception as error:
                print(error)
    else:
        formulario = PromocionModelForm()
    
    return render(request, "promocion/create.html", {"formulario":formulario})

def promocion_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSpromocion = Promocion.objects.select_related("misusuario")

            #Obtenemos los filtros

            textoBusqueda = formulario.cleaned_data.get("textoBusqueda")
            fecha_desde = formulario.cleaned_data.get("fecha_desde")
            fecha_hasta = formulario.cleaned_data.get("fecha_hasta")

            if(textoBusqueda != ""):
                QSPromocion = QSPromocion.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o descripción que contengan la palabra "+textoBusqueda+"\n"
                
            if(not fecha_desde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha_desde,'%d-%m-%Y')+"\n"
                QSlibros = QSlibros.filter(fecha_publicacion__gte=fecha_desde)
            
            if(not fecha_hasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fecha_hasta,'%d-%m-%Y')+"\n"
                QSlibros = QSlibros.filter(fecha_publicacion__lte=fecha_hasta)
            
            
            promociones = QSpromocion.all()

            return render(request, "appFutbol/listado_promociones.html", {"promociones":promociones, "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
        
    return render(request, "promocion/busqueda_avanzada.html", {"formulario":formulario})

def promocion_editar(request,promo_id):
    promo = Promocion.objects.get(id=promo_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = PromocionModelForm(datosFormulario,instance = promo)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el libro'+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('libro_lista')  
            except Exception as error:
                print(error)
    return render(request, 'promocion/actualizar.html',{"formulario":formulario,"promo":promo})
    
# Prueba mapa
#def home(request):
#    initialMap = folium.Map(location=[37.37742919500497, -5.934836071794303], zoom_start=9)
#    context = initialMap._repr_html_
#    return render(request, "appFutbol/home.html", {"context":context})
    
# Errores

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
