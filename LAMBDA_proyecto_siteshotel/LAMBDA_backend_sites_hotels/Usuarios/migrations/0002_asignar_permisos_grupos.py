from django.db import migrations


def asignar_permisos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Crear grupos si no existen
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    inversionista_group, _ = Group.objects.get_or_create(name='Inversionista')

    # Permisos para admin (todos los permisos de todos los modelos)
    admin_perms = Permission.objects.all()
    admin_group.permissions.set(admin_perms)

    # Permisos para inversionista (solo view de todos los modelos)
    view_perms = Permission.objects.filter(codename__startswith='view_')
    inversionista_group.permissions.set(view_perms)


class Migration(migrations.Migration):
    dependencies = [
        ('Usuarios', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(asignar_permisos),
    ]
