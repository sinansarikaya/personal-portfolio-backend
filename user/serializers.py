from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password 



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Passwords do not match!"})

        if get_user_model().objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Email is already in use!"})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        "required": "The email field is required.",
        "invalid": "The email address you entered is not valid. Please check and try again."
    })
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        error_messages={"required": "The password field is required."})

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Email or Password is incorrect!")
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.")
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'last_login')

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance