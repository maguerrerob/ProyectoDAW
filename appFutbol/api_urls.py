from django.urls import path
from  .api_views import *

urlpatterns = [
    # Consulta sencilla a modelo principal
    # Consulta mejorada
    path("partidos_mejorada", partido_list_mejorada),
    # URLs token oauth2 mejorada
    path("datosusuarios", datosusuarios_list),
    path("recintos/listar", recintos_list),
    # URLs token JWT
    path("posts/listar", posts_listar),
    path("recintos/busqueda_simple", recinto_busqueda_simple),
    path("recintos/busqueda_avanzada", recinto_buscar_avanzado),
    path("datosusuario/busqueda_avanzada", datosusuario_busqueda_avanzada),
    path("partidos/busqueda_avanzada", partido_buscar_avanzado),
    path("partido/crear", partido_create),
    path('partido/<int:partido_id>',partido_obtener),
    path("partido/put/<int:partido_id>", partido_put),
    path("partido/actualizar/hora/<int:partido_id>", partido_patch_hora),
    path("partido/eliminar/<int:partido_id>", partido_eliminar),
    path("recinto/create", recinto_create),
    path("recinto/<int:recinto_id>", recinto_obtener),
    path('recinto/put/<int:recinto_id>', recinto_put),
    path("recinto/actualizar/nombre/<int:recinto_id>", recinto_patch_ubicacion),
    path("recinto/eliminar/<int:recinto_id>", recinto_eliminar),
    path("clientes/listar", clientes_list),
    path("duenyosrecintos/listar", duenyosrecintos_list),
    path("datosusuario/create", datosusuario_create),
    path("datosusuario/<int:datosusuario_id>", datosusuario_obtener),
    path("datosusuario/put/<int:datosusuario_id>", datosusuario_put),
    path("datosusuario/eliminar/<int:datosusuario_id>", datosusuario_eliminar),
    path("datosusuario/actualizar_ubicacion/ubicacion/<int:datosusuario_id>", datosusuario_patch_ubicacion),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
    path('descargar/<str:nombre_archivo>/', FileDownload.as_view(), name='descargar_archivo'),
    path('eliminar-archivo/<str:nombre_archivo>/', DeleteFile.as_view(), name='eliminar_archivo'),
    path("registrar/usuario", registrar_usuario.as_view()),
    path('usuario/token/<str:token>', obtener_usuario_token)
]