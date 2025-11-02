from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """Autenticación por correo y contraseña."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get('email', username)
        print(f"[EmailBackend] Email recibido: {email}")
        try:
            user = UserModel.objects.get(email=email)
            print(f"[EmailBackend] Usuario encontrado: {user}")
        except UserModel.DoesNotExist:
            print("[EmailBackend] Usuario NO encontrado")
            return None
        if user.check_password(password):
            print("[EmailBackend] Contraseña correcta")
        else:
            print("[EmailBackend] Contraseña INCORRECTA")
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
