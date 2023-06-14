from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'First name is required.',
            'null': 'First name cannot be null.',
            'invalid': 'Invalid first name.',
        }
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            'blank': 'Last name is required.',
            'null': 'Last name cannot be null.',
            'invalid': 'Invalid last name.',
        }
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(), message="This username is already used.")],
        error_messages={
            'blank': 'Username is required.',
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.',
        }
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already used.',
            )
        ],
        error_messages={
            'blank': 'Email is required.',
            'null': 'Email cannot be null.',
            'invalid': 'Invalid email address.',
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required',
            'blank': 'Password is required.',
            'null': 'Password cannot be null.',
        }
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Password is required',
            'blank': 'Password is required.',
            'null': 'Password cannot be null.',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'password2')

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields did not match."})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )


class CustomTokenSerializer(TokenSerializer):

    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = (
            'key',
            'user',
            )