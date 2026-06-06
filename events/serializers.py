from django.utils import timezone
from rest_framework import serializers
from .models import Event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_event_date(self,value):
        if value < timezone.now().date():
            raise serializers.ValidationError('Event date cannot be in the future')

        return value

    def validate(self,attrs):
        total = attrs.get('total_seats')
        available = attrs.get('available_seats')

        if total is not None and total <= 0:
            raise serializers.ValidationError("Total seats must be greater than 0.")

        if available is not None and available < 0:
            raise serializers.ValidationError("Available seats cannot be negative.")

        if total is not None and available is not None:
            if total < available:
                raise serializers.ValidationError('Available seats cannot be greater than total seats')

        return attrs