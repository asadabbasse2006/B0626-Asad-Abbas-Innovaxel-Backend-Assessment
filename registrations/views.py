from django.db import transaction
from events.models import Event
from registrations.models import Registration
from registrations.serializers import RegistrationSerializer

from rest_framework import status, response
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class RegisterUserAPIView(APIView):
    def post(self,request):
        event_id = request.data.get('event_id')
        username = request.data.get('username')

        try:
            event = Event.objects.get(id=event_id)

        except:
            return Response(
                {
                    "error": "Event does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if Registration.objects.filter(event=event,username=username,status="ACTIVE").exists():
            return Response({"error":"User already exists for this event"},status=status.HTTP_400_BAD_REQUEST)

        if event.available_seats <= 0:
            return Response({"error":"No seats available for this event"},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():

            event = Event.objects.select_for_update().get(id=event_id)

            if event.available_seats <= 0:
                return Response(
                    {"error": "No seats available"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            registration = Registration.objects.create(
                event=event,
                username=username,
                status='ACTIVE'
            )

            event.available_seats -= 1
            event.save()

        serializer = RegistrationSerializer(registration)

        return Response(
            {
                "message": "Registration successful",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class CancelRegistrationAPIView(APIView):

    def post(self, request):
        registration_id = request.data.get('registration_id')

        try:
            registration = Registration.objects.select_related('event').get(id=registration_id)
        except:
            return Response(
                {"error": "Registration not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if registration.status == 'CANCELLED':
            return Response(
                {"error": "Registration already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():

            event = registration.event

            registration.status = 'CANCELLED'
            registration.save()

            event.available_seats += 1
            event.save()

        return Response(
            {
                "message": "Registration cancelled successfully",
                "registration_id": registration.id,
                "event_id": event.id
            },
            status=status.HTTP_200_OK
        )