from django.apps import AppConfig
from django.db.models.signals import post_migrate

def crear_roles(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    roles = {
        "Administrador": ["add_usuario", "change_usuario", "delete_usuario", "view_usuario"],
        "Inversionista": ["view_usuario"],
    }
    for nombre, perms in roles.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        for codename in perms:
            try:
                p = Permission.objects.get(codename=codename)
                grupo.permissions.add(p)
            except Permission.DoesNotExist:
                continue

class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Usuarios"
    verbose_name = "Gestión de Usuarios"

    def ready(self):
        post_migrate.connect(crear_roles, sender=self)
