from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from .models import Usuario

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    grupos = serializers.StringRelatedField(many=True, source="groups")
    tipo_usuario = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "first_name", "last_name", "grupos", "estado", "tipo_usuario"]

    def get_tipo_usuario(self, obj):
        grupos = obj.groups.values_list('name', flat=True)
        if 'Admin' in grupos:
            return 'Admin'
        elif 'Inversionista' in grupos:
            return 'Inversionista'
        return 'Sin grupo'

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    tipo_usuario = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ["id", "email", "username", "password", "tipo_usuario"]

    def create(self, datos):
        # Crear los grupos si no existen
        Group.objects.get_or_create(name="Admin")
        Group.objects.get_or_create(name="Inversionista")
        try:
            usuario = Usuario.objects.create_user(
                email=datos["email"],
                username=datos["username"],
                password=datos["password"]
            )
            tipo = datos.get("tipo_usuario", None)
            if tipo == "Admin":
                grupo = Group.objects.get(name="Admin")
                usuario.groups.add(grupo)
            elif tipo == "Inversionista":
                grupo = Group.objects.get(name="Inversionista")
                usuario.groups.add(grupo)
            usuario.save()
            return usuario
        except Exception as e:
            raise serializers.ValidationError({"error": f"Ocurrió un error al crear el usuario: {e}"})

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        usuario = authenticate(email=data["email"], password=data["password"])
        if not usuario:
            raise serializers.ValidationError("Credenciales inválidas. Verifique el email y la contraseña.")
        if not usuario.is_active:
            raise serializers.ValidationError("El usuario está inactivo.")
        return usuario

class CrearUsuarioSerializer(serializers.ModelSerializer):
    grupo = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["email", "username", "grupo"]

    def create(self, validated_data):
        grupo_nombre = validated_data.pop("grupo")
        usuario = Usuario.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            is_active=False
        )
        grupo, _ = Group.objects.get_or_create(name=grupo_nombre)
        usuario.groups.add(grupo)
        usuario.save()
        return usuario

class ActivarUsuarioSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, data):
        try:
            usuario = Usuario.objects.get(pk=data["uid"])
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no existe.")
        if not default_token_generator.check_token(usuario, data["token"]):
            raise serializers.ValidationError("Token inválido o expirado.")
        data["usuario"] = usuario
        return data
