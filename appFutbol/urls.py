from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios", views.usuarios, name="lista_usuarios"),
    path("usuario_por_posicion/<str:pos>", views.buscar_usuario, name="buscar_usuario"),
    path("partidos_usuario/<int:id_usuario>", views.partidos_usuario, name="partidos_usuario"),
    path("usuarios_partido/<int:id_partido>", views.usuarios_partido, name="usuarios_partido"),
    path("usuarios_con_n_posts/<int:n>", views.usuarios_post, name="usuarios_post"),
    path("partidos_ganados_visitantes", views.ganados_visitantes, name="ganados_visitantes"),
    path("partidos_ganados_locales", views.ganados_locales, name="ganados_locales"),
    path("sala_o_siete", views.futbol_sala_siete, name="futbol_sala_siete"),
    path("usuarios_niveles", views.niveles_usuarios, name="niveles_usuarios"),
    path("ultima_votacion/<int:id_partido>", views.ultima_votacion, name="ultima_votacion"),
    path("partidos", views.partidos_realizados, name="partidos_realizados"),
    path("votaciones_usuarios_3/<int:id_usuario>", views.votacion_3, name="votacion_3"),
    path("usuarios_sin_votaciones", views.usuarios_sin_votaciones, name="usuarios_sin_votaciones"),
    path("cuentas_bancarias/<str:nombre>", views.validar_banco, name="validar_banco"),
    path("media_votaciones", views.media_partidos, name="media_partidos"),
    path("crear_partidos", views.partido_create, name="partido_create"),
    path("recintos", views.listar_recintos, name="listar_recintos"),
    path("recinto/buscar/", views.recinto_buscar, name="recinto_buscar"),
    path("partido/buscar_avanzada", views.partido_buscar_avanzado, name="partido_buscar_avanzado")
]