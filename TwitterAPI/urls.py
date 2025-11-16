from django.urls import path
from TwitterAPI.views.users import SendEmailRegistrationApiView, CodeVerifiedAPIView, ResendCodeAPIView, FullSignUpAPIVIew


urlpatterns = [
    path('sign-up/', SendEmailRegistrationApiView.as_view()),
    path('verify/', CodeVerifiedAPIView.as_view()),
    path('resend-code/', ResendCodeAPIView.as_view()),
    path('full-singup/', FullSignUpAPIVIew.as_view())
]