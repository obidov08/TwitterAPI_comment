from django.urls import path
from TwitterAPI.views.users import SendEmailRegistrationApiView


urlpatterns = [
    path('sign-up/', SendEmailRegistrationApiView.as_view())
]