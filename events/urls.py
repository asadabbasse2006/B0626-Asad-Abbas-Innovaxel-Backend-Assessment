from django.urls import path
from .views import CreateEventAPIView,EventListAPIView

urlpatterns = [
    path('events/', CreateEventAPIView.as_view(),name='create_event'),
    path('events/list/', EventListAPIView.as_view(), name='list-events'),
]