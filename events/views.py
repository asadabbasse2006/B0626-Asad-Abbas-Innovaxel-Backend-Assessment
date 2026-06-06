from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from rest_framework.views import APIView


# Create your views here.

class CreateEventAPIView(APIView):

    def post(self, request):
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message":'Event Created successfully',
                    'data':serializer.data
                    }
                , status=status.HTTP_201_CREATED)

        return Response(
            {
                "message":'Validation Failed',
                'errors':serializer.errors
            },
        status=status.HTTP_400_BAD_REQUEST)

class EventListAPIView(APIView):

    def get(self,request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response({
            "count":events.count(),
            'results':serializer.data
        },status=status.HTTP_200_OK)
