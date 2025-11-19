from rest_framework.views import APIView
from TwitterAPI.utils import send_code_to_email
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.context_processors import request
from TwitterAPI.serializers.users import ChangePasswordRequestSerializer, CodeSerializer, EmailSerializer, FullSignUpSerializer, LoginSerializer, validate
from TwitterAPI.models import User, CODE_VERIFIED, DONE
from rest_framework import serializers, status
from TwitterAPI.utils import CustomResponse
from TwitterAPI.models.users import User, ChangePassword
from config.settings import EMAIL_HOST_USER


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
        if user.status not in [CODE_VERIFIED, DONE]:
            return CustomResponse.error(
                status=False,
                message="You are not verified."
            )
        
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
        

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_name = serializer.validated_data.get('user_input')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            return CustomResponse.success(
                status=True,
                message='You are logged in success!',
            )
        return CustomResponse.success(status=True, message='ozodbek')
    
class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.User
        confirmations = user.confirmations.order_by("-created_at").first()
        if confirmations.is_expired():
            return CustomResponse.error(
                status=True, 
                message='The code has not expired.'
            )
        
        send_code_to_email(user.email, code=user.create_verified_code())

        return CustomResponse.success(
            status=True,
            message='A verification code has been send to your email.',
            token = user.token()
        )
    

class ChangePasswordRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.User

        ChangePassword.objects.filter(user=user, is_active=True).update(is_active=False)
        
        change_password_obj = ChangePassword.objects.create(user=user)

        reset_url = f"http://127.0.0.1:8000/twitter/change-password/?token={change_password_obj.token}"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password: {reset_url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

        return CustomResponse.success(
            status=True,
            message='Password reset link has been sent your email.',
            data={"token": change_password_obj.token}
        )
    

class ChangePasswordView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = ChangePasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        new_pasword = serializer.validated_data['new_password']

        try:
            change_password_obj = ChangePassword.objects.get(token=token, is_active=True)
        except ChangePassword.DoesNotExist:
            return CustomResponse.error(
                status=False,
                message="Invalid or expired token."
            )
        
        user = change_password_obj.user
        user.set_password(new_pasword)
        user.save()

        change_password_obj.deactivate()

        return CustomResponse.success(
            status=True,
            message='Password has been change successfuly.',
            data={"username": user.username}
        )