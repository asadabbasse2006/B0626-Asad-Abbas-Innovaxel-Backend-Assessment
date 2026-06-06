from django.urls import path
from .views import RegisterUserAPIView,CancelRegistrationAPIView

urlpatterns = [
    path('register/',RegisterUserAPIView.as_view(),name='register_user'),
    path('cancel/', CancelRegistrationAPIView.as_view()),

]