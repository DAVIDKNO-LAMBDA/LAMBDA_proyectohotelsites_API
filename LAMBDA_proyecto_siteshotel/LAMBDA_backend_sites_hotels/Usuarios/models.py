from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    estado = models.BooleanField(default=True, verbose_name="Estado del usuario")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modificado = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]  
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "usuarios"

    def __str__(self):
        return f"{self.username} - {self.email}"
    
    @property
    def get_estado(self):
        return "Activo" if self.estado else "Inactivo"
