from rest_framework import serializers, status
from TwitterAPI.models import User, DONE
import re


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) 

    def validate_email(self, email):

        if not email:
            raise serializers.ValidationError("Email maydoni bo'sh bo'lishi mumkin emas")

        if User.objects.filter(email=email).filter(status=DONE).exists():
            data = {
                "status": False,
                "message": "This email already exists."
            }
            raise serializers.ValidationError(data)
        return email
    
class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

    def validate_code(self, code):
        if not re.fullmatch(r"\d{4}", code):
            raise serializers.ValidationError("The code must consist of 4 digit.")
        return code


class FullSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    reset_password = serializers.CharField(required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User is already exist!")
        return username
    
    def valdate_reset_password(self, validated_data):
        password = validated_data.get("password")
        reset_password = validated_data.get('reset_password')
        if password != reset_password:
            raise serializers.ValidationError("Password don't match")
        return validated_data