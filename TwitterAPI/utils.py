from django.core.mail import send_mail
from rest_framework.response import Response
from config.settings import EMAIL_HOST_USER
from rest_framework import status as st
import re


def send_code_to_email(email, code):
    text = f"Assalomu aleykum, TwitterAPI uchun tasdiqlash kodi kiriting: {code}"
    send_mail(
        subject="Confirmation code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


class CustomResponse:
    @staticmethod
    def success(status, message, data=None):
        response_data = {
            "status": status,
            "message": message,
            "data": data,
        }
        return Response(
            data=response_data,
            status=st.HTTP_200_OK
        )
    
    @staticmethod
    def error(status, message, data=None):
        response_data = {
            "status": status,
            "message": message,
            "data": data,
        }
        return Response(
            data=response_data,
            status=st.HTTP_400_BAD_REQUEST,
        )
    
def username_or_email(user_input: str):
    return re.match(r'[a-zA-Z0-9._%+-]@[a-zA-Z0-9.-]+\.[a-zA-Z]{2, }$', user_input)