from rest_framework.views import APIView
from TwitterAPI.utils import send_code_to_email
from rest_framework.response import Response
from rest_framework import serializers
from TwitterAPI.serializers.users import EmailSerializer
from TwitterAPI.models import User

class SendEmailRegistrationApiView(APIView):
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        email = request.data.get("email")
        user = User.objects.create(
            email=email
        )
        send_code_to_email(email, user.create_verified_code())

        data = {
            "status": True,
            "message": "Confirmation code has sent to you email.",
            "token": user.token()
        }

        return Response(data)
    
