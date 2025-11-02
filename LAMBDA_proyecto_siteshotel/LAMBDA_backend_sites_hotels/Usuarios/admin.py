from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("id", "username", "email", "is_active", "estado")
    ordering = ("id",)
    search_fields = ("username", "email")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas importantes", {"fields": ("last_login",)}),
    )
    add_fieldsets = ((None, {"classes": ("wide",),
        "fields": ("email", "username", "password1", "password2", "is_staff", "is_active")}),)
