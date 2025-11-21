from django.urls import path
from TwitterAPI.views import ChangePasswordView, CodeVerifiedAPIView, FullSignUpAPIVIew, ResendCodeAPIView, SendEmailRegistrationApiView,\
    LoginAPIView, ChangePasswordRequestView, CreatedPostAPIView, UpdateDeleteAPIView, CreatedMediaAPIView, DeleteMediaAPIView


urlpatterns = [
    path('sign-up/', SendEmailRegistrationApiView.as_view()),
    path('verify/', CodeVerifiedAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('full-singup/', FullSignUpAPIVIew.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('change-password-request/', ChangePasswordRequestView.as_view()), 
    path('change-password/', ChangePasswordView.as_view()),

    #Post
    path('post/', CreatedPostAPIView.as_view()),
    path('update-delete/', UpdateDeleteAPIView.as_view()),
    path('media/', CreatedMediaAPIView.as_view()),
    path('delete-media/<int:pk>/', DeleteMediaAPIView.as_view())
]   
