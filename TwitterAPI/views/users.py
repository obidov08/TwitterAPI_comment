from rest_framework.views import APIView
from TwitterAPI.utils import send_code_to_email
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from TwitterAPI.serializers.users import CodeSerializer, EmailSerializer, FullSignUpSerializer
from TwitterAPI.models import User, CODE_VERIFIED, DONE
from rest_framework import status
from TwitterAPI.utils import CustomResponse


class SendEmailRegistrationApiView(APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": "Validation error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        
        try:
            user = User(email=email)
            user.save()
            
            send_code_to_email(email, user.create_verified_code())

            return CustomResponse.success(
                status=True,
                message="Confirmation code has been sent to your email.",
                data = user.token()
            )
            
        except Exception as e:
            return Response({
                "status": False,
                "message": f"Error creating user: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        

class CodeVerifiedAPIView(APIView):
    serializer_class = CodeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')
        if self.verified_code(user, code):
            return CustomResponse.success(
                status=True,
                message="Code verified successfully",
                data=user.token()
            )
        
        return CustomResponse.error(
            status=False,
            message="Code don't match or code expired"
        )

    def verified_code(self, user: User, code: str):
        confirmation = user.confirmations.order_by('-created_at').first()
        if confirmation.code == code and not confirmation.is_expired():
            user.status = CODE_VERIFIED
            user.save()  
            return True
        return False
        
class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        confirmation = user.confirmations.order_by("-created_at").first()

        if not confirmation.is_expired():
            return CustomResponse.error(
                status=False,
                message="Code has not been expired"
            )
        
        send_code_to_email(user.email, user.create_verified_code())

        return CustomResponse.success(
            status=True,
            message="Confirmation code has been sent to your email.",
            data = user.token()
        )
    

class FullSignUpAPIVIew(APIView):
    serializer_class = FullSignUpSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.status = DONE
        user.save()

        data ={
            "first_name": first_name,
            "last_name ": last_name,
            "username": username,
            "email": user.email
        }

        return CustomResponse.success(
            status=True,
            message="User has been registered successfully",
            data=data
        )
        