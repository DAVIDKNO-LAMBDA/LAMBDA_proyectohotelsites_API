from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegistroSerializer, LoginSerializer, UsuarioSerializer, CrearUsuarioSerializer, ActivarUsuarioSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

Usuario = get_user_model()

class RegistrarUsuario(APIView):
    permission_classes = [permissions.AllowAny]  # Cambiado a AllowAny para permitir registro público

    def post(self, request):
        try:
            serializer = RegistroSerializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.save()
                return Response({
                    "mensaje": "Usuario registrado exitosamente.",
                    "usuario": UsuarioSerializer(usuario).data
                }, status=status.HTTP_201_CREATED)
            return Response({"errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error inesperado al registrar: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginUsuario(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.validated_data
                refresh = RefreshToken.for_user(usuario)
                roles = [g.name for g in usuario.groups.all()]
                return Response({
                    "mensaje": "Inicio de sesión exitoso.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": UsuarioSerializer(usuario).data,
                    "roles": roles
                }, status=status.HTTP_200_OK)
            return Response({"errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error en el inicio de sesión: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PerfilUsuario(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            usuario = request.user
            roles = [g.name for g in usuario.groups.all()]
            return Response({
                "usuario": UsuarioSerializer(usuario).data,
                "roles": roles
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al obtener perfil: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CrearUsuarioAdmin(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Solo admin puede crear usuarios
        if not request.user.groups.filter(name="Admin").exists():
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CrearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            token = default_token_generator.make_token(usuario)
            activation_link = f"http://localhost:8080/activar-cuenta?uid={usuario.pk}&token={token}"
            send_mail(
                "Activa tu cuenta",
                f"Haz clic en el siguiente enlace para activar tu cuenta y establecer tu contraseña: {activation_link}",
                "no-reply@hotels.com",
                [usuario.email],
                fail_silently=False,
            )
            return Response({"mensaje": "Usuario creado y email de activación enviado."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivarUsuario(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ActivarUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data["usuario"]
            password = serializer.validated_data["password"]
            usuario.set_password(password)
            usuario.is_active = True
            usuario.save()
            return Response({"mensaje": "Cuenta activada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
