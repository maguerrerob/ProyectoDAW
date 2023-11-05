from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios", views.usuarios, name="lista_usuarios"),
    path("usuario_por_posicion/<str:pos>", views.buscar_usuario, name="buscar_usuario"),
    path("reservas_usuario/<int:id_usuario>", views.reservas_usuario, name="reservas_usuario"),
    path("usuarios_partido/<int:id_partido>", views.usuarios_partido, name="usuarios_partido"),
    path("usuarios_con_n_posts/<int:n>", views.usuarios_post, name="usuarios_post"),
    path("partidos_ganados_visitantes", views.ganados_visitantes, name="ganados_visitantes"),
    path("partidos_ganados_locales", views.ganados_locales, name="ganados_locales"),
    path("sala_o_siete", views.futbol_sala_siete, name="futbol_sala_siete")
]