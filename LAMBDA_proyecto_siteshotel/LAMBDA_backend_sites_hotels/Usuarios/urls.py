from django.urls import path
from .views import RegistrarUsuario, LoginUsuario, PerfilUsuario, CrearUsuarioAdmin, ActivarUsuario

urlpatterns = [
    path("registrar/", RegistrarUsuario.as_view(), name="registrar_usuario"),
    path("login/", LoginUsuario.as_view(), name="login_usuario"),
    path("perfil/", PerfilUsuario.as_view(), name="perfil_usuario"),
    path("crear/", CrearUsuarioAdmin.as_view(), name="crear-usuario-admin"),
    path("activar/", ActivarUsuario.as_view(), name="activar-usuario"),
]
