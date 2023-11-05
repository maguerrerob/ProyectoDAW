from django.urls import path, re_path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usuarios", views.usuarios, name="lista_usuarios"),
    path("usuario_por_posicion/<str:pos>", views.buscar_usuario, name="buscar_usuario"),
    path("reservas_usuario/<int:id_usuario>", views.reservas_usuario, name="reservas_usuario")
]